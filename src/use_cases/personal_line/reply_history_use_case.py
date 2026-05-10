from datetime import datetime
from typing import Dict

import japanize_matplotlib  # noqa: F401

from application_service import (
    graph_service,
    message_service,
    reply_service,
    request_info_service,
)
from domain_service import (
    match_service,
    user_match_service,
)
from repositories import (
    group_repository,
    hanchan_repository,
    user_group_repository,
    user_repository,
)


class ReplyHistoryUseCase:
    def execute(self) -> None:
        req_line_id = request_info_service.req_line_user_id

        users = user_repository.find(
            query={"line_user_id": req_line_id},
        )
        if len(users) == 0:
            reply_service.add_message(
                "ユーザーが登録されていません。友達追加してください。",
            )
            reply_service.add_message(
                "既に友達の場合は一度ブロックして、ブロック解除を行ってください。",
            )
            return

        g_param = request_info_service.params.get("g")

        if g_param is None:
            user_groups = user_group_repository.find({"line_user_id": req_line_id})
            if len(user_groups) >= 2:
                group_ids = [ug.line_group_id for ug in user_groups]
                groups = group_repository.find({"line_group_id": {"$in": group_ids}})
                reply_service.add_personal_history_group_quick_reply(groups)
                return
            g_param = "all"

        from_dt, to_dt, is_valid = message_service.parse_date_range_from_params(
            request_info_service.params,
        )
        if not is_valid:
            for msg in message_service.DATE_FORMAT_ERROR_MESSAGES:
                reply_service.add_message(msg)
            return
        um_list = user_match_service.find_all_by_user_id_list(
            [users[0]._id],
            from_dt=from_dt,
            to_dt=to_dt,
        )
        if g_param != "all":
            matches = match_service.find_all_by_ids_and_line_group_ids(
                ids=[um.match_id for um in um_list],
                line_group_ids=[g_param],
            )
        else:
            matches = match_service.find_all_for_graph(
                ids=[um.match_id for um in um_list],
            )

        if len(matches) == 0:
            reply_service.add_message(
                "対局履歴がありません。",
            )
            return
        all_hanchans = hanchan_repository.find(
            query={"match_id": {"$in": [match._id for match in matches]}},
        )

        if len(all_hanchans) == 0:
            error_message = "半荘情報を取得できませんでした。"
            raise ValueError(error_message)

        range_message = message_service.create_range_message(from_dt, to_dt)
        if range_message is not None:
            reply_service.add_message(range_message)

        message = ""
        total = 0

        # グラフ描画用プロットデータ
        history: Dict[datetime, int] = {}

        for match in matches:
            score = 0
            for hanchan in [
                hanchan for hanchan in all_hanchans if hanchan.match_id == match._id
            ]:
                if req_line_id in hanchan.converted_scores:
                    score += hanchan.converted_scores[req_line_id]
            total += score
            str_score = ("+" + str(score)) if score > 0 else str(score)
            message += match.created_at.strftime("%Y/%m/%d") + ": " + str_score + "\n"

            history[match.created_at] = total

        # 今までの全半荘一覧
        reply_service.add_message(
            message,
        )

        # 合計
        str_total = ("+" + str(total)) if total > 0 else str(total)
        reply_service.add_message(
            "累計: " + str_total,
        )

        # グラフ描画
        fig = graph_service.build_history_step_graph(
            histories={req_line_id: history},
            start_date=matches[0].created_at,
            to_dt=to_dt,
            match_count=len(matches),
        )

        path = f"/personal_history/{req_line_id}.png"
        url, err = graph_service.save_figure(fig, path)
        if err:
            reply_service.create_and_reply_file_upload_error("対戦履歴", req_line_id)
            return
        reply_service.add_image(url)
