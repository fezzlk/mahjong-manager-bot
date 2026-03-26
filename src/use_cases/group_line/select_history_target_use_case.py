from application_service import reply_service, request_info_service
from domain_model.entities.history_session import HistorySession
from domain_service import user_group_service, user_service
from repositories import history_session_repository

_TIMEOUT_MSG = "タイムアウトしました。その他メニューの「成績推移」から再度お試しください。"


class SelectHistoryTargetUseCase:
    def execute(self) -> None:
        target = request_info_service.params.get("t", "")
        group_id = request_info_service.req_line_group_id
        requester_id = request_info_service.req_line_user_id

        if target == "self":
            session = HistorySession(
                line_group_id=group_id,
                requester_line_id=requester_id,
                selected_line_ids=[requester_id],
            )
            history_session_repository.create(session)
            reply_service.add_history_period_quick_reply()

        elif target == "all":
            user_groups = user_group_service.find_all_by_line_group_id(group_id)
            all_ids = [ug.line_user_id for ug in user_groups]
            session = HistorySession(
                line_group_id=group_id,
                requester_line_id=requester_id,
                selected_line_ids=all_ids,
            )
            history_session_repository.create(session)
            reply_service.add_history_period_quick_reply()

        elif target == "select":
            session = HistorySession(
                line_group_id=group_id,
                requester_line_id=requester_id,
                selected_line_ids=[],
            )
            history_session_repository.create(session)
            _show_user_select_carousel(group_id, [])

        else:
            reply_service.add_message("不正なリクエストです。")


def _show_user_select_carousel(group_id: str, selected_ids: list) -> None:
    user_groups = user_group_service.find_all_by_line_group_id(group_id)
    members = []
    for ug in user_groups:
        user = user_service.find_one_by_line_user_id(ug.line_user_id)
        if user is not None:
            members.append(user)
    reply_service.add_history_user_select_carousel(members, selected_ids)
