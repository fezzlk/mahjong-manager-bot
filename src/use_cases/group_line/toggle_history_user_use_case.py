from application_service import reply_service, request_info_service
from domain_service import user_group_service, user_service
from repositories import history_session_repository

_TIMEOUT_MSG = "タイムアウトしました。その他メニューの「成績推移」から再度お試しください。"


class ToggleHistoryUserUseCase:
    def execute(self) -> None:
        group_id = request_info_service.req_line_group_id
        user_id = request_info_service.params.get("u", "")

        session = history_session_repository.find_active_by_group_id(group_id)
        if session is None:
            reply_service.add_message(_TIMEOUT_MSG)
            return

        selected = list(session.selected_line_ids)
        if user_id in selected:
            selected.remove(user_id)
        elif len(selected) < 10:
            selected.append(user_id)

        history_session_repository.update_selected_users(group_id, selected)

        user_groups = user_group_service.find_all_by_line_group_id(group_id)
        members = []
        for ug in user_groups:
            user = user_service.find_one_by_line_user_id(ug.line_user_id)
            if user is not None:
                members.append(user)
        reply_service.add_history_user_select_carousel(members, selected)
