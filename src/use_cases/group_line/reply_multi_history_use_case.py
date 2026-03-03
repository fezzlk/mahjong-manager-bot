from datetime import datetime, timedelta
from typing import Dict, List

import japanize_matplotlib  # noqa: F401
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from application_service import (
    graph_service,
    reply_service,
    request_info_service,
    message_service,
)
from domain_service import (
    user_service,
    match_service,
    user_match_service,
)

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

        if request_info_service.is_mention_all:
            reply_service.add_message(
                "@Allによるメンションでは、このグループでの対戦に参加したことのある全ユーザを対象とします。"
            )

        # 関連する対戦結果の取得
        from_dt, to_dt, is_valid = message_service.parse_date_range_from_params(
            request_info_service.params,
        )
        if not is_valid:
            for msg in message_service.DATE_FORMAT_ERROR_MESSAGES:
                reply_service.add_message(msg)
            return
        umList = user_match_service.find_all_by_user_id_list(
            target_user_ids,
            from_dt=from_dt,
            to_dt=to_dt,
        )
        matches = match_service.find_all_for_graph(
            ids=[um.match_id for um in umList],
        )

        if len(matches) == 0:
            reply_service.add_message("対局履歴がありません。")
            return

        range_message = message_service.create_range_message(from_dt, to_dt)
        if range_message is not None:
            reply_service.add_message(range_message)

        # 対戦結果の累計を計算
        total_dict = {line_id: 0 for line_id in active_user_line_ids}
        start_date = matches[0].created_at
        end_date = matches[-1].created_at
        history_dict = {
            line_id: {
                start_date - timedelta(minutes=2): 0,
                start_date - timedelta(minutes=1): 0,
            }
            for line_id in active_user_line_ids
        }
        for match in matches:
            for line_id, score in match.sum_scores.items():
                if line_id in active_user_line_ids:
                    total_dict[line_id] += score
                    history_dict[line_id][match.created_at] = total_dict[line_id]
        if to_dt is None:
            to_dt = datetime.now()
        for line_id, score in total_dict.items():
            history_dict[line_id][to_dt] = score

        # グラフ描画
        fig, ax = plt.subplots()
        for line_id in active_user_line_ids:
            plt.step(
                history_dict[line_id].keys(),
                history_dict[line_id].values(),
                where="post",
                label=line_id_name_dict[line_id],
            )

        plt.grid(which="major", axis="y")
        plt.xlim(
            [
                start_date - timedelta(minutes=1),
                end_date
                + timedelta(seconds=(end_date - start_date).total_seconds() // 100),
            ]
        )
        plt.xticks(rotation=30)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H時"))
        plt.legend()
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["top"].set_visible(False)

        path = f"/group_history/{req_line_user_id}.png"
        url, err = graph_service.save_figure(fig, path)
        if err:
            sender = (
                user_service.get_name_by_line_user_id(req_line_user_id)
                or req_line_user_id
            )
            reply_service.create_and_reply_file_upload_error("対戦履歴", sender)
            return
        reply_service.add_image(url)
