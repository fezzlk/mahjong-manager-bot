from application_service import reply_service, request_info_service
from domain_service import match_service
from repositories import match_sum_session_repository

_TIMEOUT_MSG = "タイムアウトしました。「対戦履歴」の「まとめて精算」から再度お試しください。"


class ToggleSumMatchUseCase:
    def execute(self) -> None:
        """_sum_matches_toggle?to=<match_id>: 選択状態をトグルし選択UIを再表示する。"""
        line_group_id = request_info_service.req_line_group_id
        requester_line_id = request_info_service.req_line_user_id
        match_id = request_info_service.params.get("to", "")

        session = match_sum_session_repository.find_active(line_group_id, requester_line_id)
        if session is None:
            reply_service.add_message(_TIMEOUT_MSG)
            return

        selected = list(session.selected_match_ids)
        if match_id in selected:
            selected.remove(match_id)
        else:
            selected.append(match_id)

        match_sum_session_repository.update_selected_matches(line_group_id, requester_line_id, selected)

        archived_matches = match_service.find_all_archived_by_line_group_id(line_group_id=line_group_id)
        recent = archived_matches[-10:]
        start_index = len(archived_matches) - len(recent) + 1
        reply_service.add_sum_matches_select_quick_reply(recent, start_index, selected)
