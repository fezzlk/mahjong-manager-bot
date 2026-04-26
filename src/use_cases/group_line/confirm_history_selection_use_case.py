from application_service import reply_service, request_info_service
from domain_service import user_group_service, user_service
from repositories import history_session_repository

_TIMEOUT_MSG = "タイムアウトしました。その他メニューの「成績推移」から再度お試しください。"


class ConfirmHistorySelectionUseCase:
    def execute(self) -> None:
        group_id = request_info_service.req_line_group_id

        session = history_session_repository.find_active_by_group_id(group_id)
        if session is None:
            reply_service.add_message(_TIMEOUT_MSG)
            return

        if not session.selected_line_ids:
            user_groups = user_group_service.find_all_by_line_group_id(group_id)
            members = []
            for ug in user_groups:
                user = user_service.find_one_by_line_user_id(ug.line_user_id)
                if user is not None:
                    members.append(user)
            reply_service.add_message("ユーザを選んでください。")
            reply_service.add_history_user_select_carousel(members, [])
            return

        reply_service.add_history_period_quick_reply()
