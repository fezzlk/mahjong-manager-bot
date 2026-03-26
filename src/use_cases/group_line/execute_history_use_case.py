import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

import japanize_matplotlib  # noqa: F401

from application_service import (
    graph_service,
    reply_service,
    request_info_service,
)
from domain_service import (
    match_service,
    user_match_service,
    user_service,
)
from repositories import history_session_repository

logger = logging.getLogger(__name__)
_TIMEOUT_MSG = "タイムアウトしました。その他メニューの「成績推移」から再度お試しください。"


def _period_to_date_range(period: str) -> Tuple[Optional[datetime], Optional[datetime]]:
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    if period == "month":
        from_dt = today.replace(day=1)
        return from_dt, None
    if period == "last_month":
        first_of_this_month = today.replace(day=1)
        last_month = first_of_this_month - timedelta(days=1)
        from_dt = last_month.replace(day=1)
        return from_dt, first_of_this_month
    if period == "3months":
        from_dt = today - timedelta(days=90)
        return from_dt, None
    if period == "6months":
        from_dt = today - timedelta(days=180)
        return from_dt, None
    # "all"
    return None, None


class ExecuteHistoryUseCase:
    def execute(self) -> None:
        group_id = request_info_service.req_line_group_id
        requester_id = request_info_service.req_line_user_id
        period = request_info_service.params.get("p", "all")

        session = history_session_repository.find_active_by_group_id(group_id)
        if session is None:
            logger.warning("history session timeout or not found: group=%s", group_id)
            reply_service.add_message(_TIMEOUT_MSG)
            return

        target_line_ids = session.selected_line_ids
        if not target_line_ids:
            reply_service.add_message("対象ユーザが選択されていません。")
            history_session_repository.delete_by_group_id(group_id)
            return

        from_dt, to_dt = _period_to_date_range(period)

        target_user_ids = []
        active_line_ids = []
        line_id_name_dict: Dict[str, str] = {}
        contain_not_friend_user = False

        for line_id in target_line_ids:
            user = user_service.find_one_by_line_user_id(line_id)
            if user is None:
                contain_not_friend_user = True
                continue
            line_id_name_dict[user.line_user_id] = user.line_user_name
            active_line_ids.append(user.line_user_id)
            target_user_ids.append(user._id)

        if contain_not_friend_user:
            reply_service.add_message("友達登録されていないユーザは表示されません。")

        if not target_user_ids:
            reply_service.add_message("対局履歴がありません。")
            history_session_repository.delete_by_group_id(group_id)
            return

        um_list = user_match_service.find_all_by_user_id_list(
            target_user_ids,
            from_dt=from_dt,
            to_dt=to_dt,
        )
        matches = match_service.find_all_for_graph(
            ids=[um.match_id for um in um_list],
        )

        if not matches:
            reply_service.add_message("対局履歴がありません。")
            history_session_repository.delete_by_group_id(group_id)
            return

        total_dict = dict.fromkeys(active_line_ids, 0)
        history_dict: Dict[str, Dict[datetime, int]] = {
            line_id: {} for line_id in active_line_ids
        }
        for match in matches:
            for line_id, score in match.sum_scores.items():
                if line_id in active_line_ids:
                    total_dict[line_id] += score
                    history_dict[line_id][match.created_at] = total_dict[line_id]

        is_single = len(active_line_ids) == 1
        fig = graph_service.build_history_step_graph(
            histories=history_dict,
            start_date=matches[0].created_at,
            to_dt=to_dt,
            line_id_name_dict=line_id_name_dict if not is_single else None,
            match_count=len(matches) if is_single else None,
        )

        path = f"/group_history/{requester_id}.png"
        url, err = graph_service.save_figure(fig, path)
        if err:
            sender = (
                user_service.get_name_by_line_user_id(requester_id) or requester_id
            )
            reply_service.create_and_reply_file_upload_error("対戦履歴", sender)
            history_session_repository.delete_by_group_id(group_id)
            return

        reply_service.add_image(url)
        history_session_repository.delete_by_group_id(group_id)
