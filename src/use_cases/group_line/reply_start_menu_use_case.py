from application_service import (
    reply_service,
    request_info_service,
)
from domain_service import match_service


class ReplyStartMenuUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        has_open_match = len(match_service.find_all_open_by_line_group_id(line_group_id)) > 0
        reply_service.add_start_menu(has_open_match=has_open_match)
