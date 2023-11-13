from typing import Dict, List
from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainService import (
    user_service,
    match_service,
    user_match_service,
)
import env_var
from messaging_api_setting import line_bot_api

# flake8: noqa
import japanize_matplotlib


class ReplyMultiHistoryUseCase:

    def execute(self) -> None:
        req_line_user_id = request_info_service.req_line_user_id
        mention_line_user_ids = request_info_service.mention_line_ids
        messages = []
        target_user_ids: List[int] = []
        active_user_line_ids: List[str] = []
        line_id_name_dict: Dict[str, str] = {}
        contain_not_friend_user = False

        mention_line_user_ids.append(req_line_user_id)

        # 表示対象のユーザ情報の取得
        for mention_line_user_id in set(mention_line_user_ids):
            user = user_service.find_one_by_line_user_id(mention_line_user_id)

            if user is None:
                contain_not_friend_user = True
                continue

            line_id_name_dict[user.line_user_id] = user.line_user_name
            active_user_line_ids.append(user.line_user_id)
            target_user_ids.append(user._id)

        if contain_not_friend_user:
            reply_service.add_message("友達登録されていないユーザは表示されません。")

        # 関連する対戦結果の取得
        umList = user_match_service.find_all_by_user_id_list(target_user_ids)
        matches = match_service.find_all_for_graph(
            ids=[um.match_id for um in umList],
        )

        if len(matches) == 0:
            reply_service.add_message(
                '対局履歴がありません。'
            )
            return

        # 対戦結果の累計を計算
        from datetime import timedelta
        total_dict = {line_id: 0 for line_id in active_user_line_ids}
        start_date = matches[0].created_at
        end_date = matches[-1].created_at
        history_dict = {line_id: {
            start_date - timedelta(minutes=2): 0,
            start_date - timedelta(minutes=1): 0,
        } for line_id in active_user_line_ids}
        for match in matches:
            for line_id, score in match.sum_scores.items():
                if line_id in active_user_line_ids:
                    total_dict[line_id] += score
                    history_dict[line_id][match.created_at] = total_dict[line_id]

        # グラフ描画
        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        matplotlib.use('agg')

 
        fig, ax = plt.subplots()
        for line_id in active_user_line_ids:
            plt.step(
                history_dict[line_id].keys(),
                history_dict[line_id].values(),
                where='post',
                label=line_id_name_dict[line_id])
            
        plt.grid(which='major', axis='y')
        plt.xlim([start_date - timedelta(minutes=1), end_date])
        plt.xticks(rotation=30)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H時"))
        plt.legend()

        try:
            fig.savefig(f"src/uploads/group_history/{req_line_user_id}.png")
        except FileNotFoundError:
            reply_service.reset()
            reply_service.add_message(text='システムエラーが発生しました。')
            messages = [
                '対戦履歴の画像アップロードに失敗しました',
                '送信者: ' + user_service.get_name_by_line_user_id(req_line_user_id) or req_line_user_id,
            ]
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message='\n'.join(messages),
            )
            return
        plt.clf()
        plt.close()

        path = f'uploads/group_history/{req_line_user_id}.png'
        image_url = f'{env_var.SERVER_URL}{path}'
        reply_service.add_image(image_url)
