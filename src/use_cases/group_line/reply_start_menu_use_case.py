from application_service import (
    reply_service,
    request_info_service,
)
from domain_service import match_service


class ReplyStartMenuUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        has_open_match = match_service.has_open_match(line_group_id)
        reply_service.add_start_menu(has_open_match=has_open_match)
