from datetime import datetime
import env_var
from ApplicationService import (
    request_info_service,
    reply_service,
    message_service,
)
from repositories import (
    user_repository,
    hanchan_repository,
)
from DomainService import (
    user_match_service,
    match_service,
)


class ReplyHistoryUseCase:

    def execute(self) -> None:
        req_line_id = request_info_service.req_line_user_id

        users = user_repository.find(
            query={'line_user_id': req_line_id},
        )
        if len(users) == 0:
            reply_service.add_message(
                'ユーザーが登録されていません。友達追加してください。'
            )
            reply_service.add_message(
                '既に友達の場合は一度ブロックして、ブロック解除を行ってください。'
            )
            return
        from_str = request_info_service.params.get('from')
        to_str = request_info_service.params.get('to')
        from_dt, from_is_invalid = message_service.parse_date_from_text(from_str)
        to_dt, to_is_invalid = message_service.parse_date_from_text(to_str)
        if from_is_invalid or to_is_invalid:
            reply_service.add_message('日付は以下のフォーマットで入力してください。')
            reply_service.add_message('[日付の入力方法]\n\nYYYY年MM月DD日\n→ YYYYMMDD\n\n20YY年MM月DD日\n→ YYMMDD\n\n今年MM月DD日\n→ MMDD\n\n今月DD日\n→ DD')
            return
        umList = user_match_service.find_all_by_user_id_list(
            [users[0]._id],
            from_dt=from_dt,
            to_dt=to_dt,
        )
        matches = match_service.find_all_for_graph(
            ids=[um.match_id for um in umList],
        )

        if len(matches) == 0:
            reply_service.add_message(
                '対局履歴がありません。'
            )
            return
        all_hanchans = hanchan_repository.find(
            query={'$and': [
                {'match_id': {'$in': [match._id for match in matches]}},
                {'status': 2},
            ]},
        )

        if len(all_hanchans) == 0:
            raise ValueError('半荘情報を取得できませんでした。')

        range_message = message_service.create_range_message(from_dt, to_dt)
        if range_message is not None:
            reply_service.add_message(range_message)

        message = ''
        total = 0

        # グラフ描画用プロットデータ
        history = {}

        for match in matches:
            score = 0
            for hanchan in [hanchan for hanchan in all_hanchans if hanchan.match_id == match._id]:
                if req_line_id in hanchan.converted_scores:
                    score += hanchan.converted_scores[req_line_id]
            total += score
            strScore = ('+' + str(score)) if score > 0 else str(score)
            message += match.created_at.strftime(
                "%Y/%m/%d") + ': ' + strScore + '\n'

            history[match.created_at] = total

        # 今までの全半荘一覧
        reply_service.add_message(
            message
        )

        # 合計
        strTotal = ('+' + str(total)) if total > 0 else str(total)
        reply_service.add_message(
            '累計: ' + strTotal
        )

        # グラフ描画
        # 初回値に0を追加、最後尾には指定された範囲の最終日または現在時点のスコアを追加
        from datetime import timedelta
        if to_dt is None:
            to_dt = datetime.now()
        history[to_dt] = total

        start_date: datetime = min(history.keys())
        end_date: datetime = max(history.keys())
        history[start_date - timedelta(minutes=2)] = 0
        history[start_date - timedelta(minutes=1)] = 0
        history = dict(sorted(history.items()))
        
        x =[]
        y =[]
        for k, v in history.items():
            x.append(k)
            y.append(v)

        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        matplotlib.use('agg')

        fig, ax = plt.subplots()
        plt.step(history.keys(), history.values(), where='mid')

        plt.grid(which='major', axis='y')
        plt.xlim([start_date - timedelta(minutes=2), end_date + timedelta(seconds=(end_date-start_date).total_seconds() // 100)])
        plt.xticks(rotation=30)
        # locator = mdates.DayLocator()
        # ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H時"))
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)

        try:
            fig.savefig(f"src/uploads/personal_history/{req_line_id}.png")
        except FileNotFoundError:
            reply_service.create_and_reply_file_upload_error('対戦履歴', req_line_id)
            return
        plt.clf()
        plt.close()

        path = f'uploads/personal_history/{req_line_id}.png'
        image_url = f'{env_var.SERVER_URL}{path}'
        reply_service.add_image(image_url)
