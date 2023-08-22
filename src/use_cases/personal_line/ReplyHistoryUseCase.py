from datetime import datetime
import env_var
from ApplicationService import request_info_service, reply_service
from repositories import (
    user_match_repository,
    user_repository,
    match_repository,
    hanchan_repository,
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
        
        umList = user_match_repository.find(
            query={'user_id': users[0]._id},
        )
        matches = match_repository.find(
            query={'$and': [
                {'_id': {'$in': [um.match_id for um in umList]}},
                {'status': 2},
            ]},
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
        # 初回値に0を追加
        from datetime import timedelta
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
        plt.xlim([start_date - timedelta(minutes=2), end_date])
        plt.xticks(rotation=30)
        # locator = mdates.DayLocator()
        # ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H時"))

        try:
            fig.savefig(f"src/uploads/personal_history/{req_line_id}.png")
        except FileNotFoundError:
            reply_service.reset()
            reply_service.add_message(text='システムエラーが発生しました。')
            messages = [
                '対戦履歴の画像アップロードに失敗しました',
                '送信者: ' + req_line_id,
            ]
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message='\n'.join(messages),
            )
            return
        plt.clf()
        plt.close()

        path = f'uploads/personal_history/{req_line_id}.png'
        image_url = f'{env_var.SERVER_URL}{path}'
        reply_service.add_image(image_url)
