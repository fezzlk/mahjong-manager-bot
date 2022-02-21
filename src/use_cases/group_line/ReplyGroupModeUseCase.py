from services import (
    request_info_service,
    group_service,
    reply_service,
)


class ReplyGroupModeUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        mode = group_service.get_mode(line_group_id)
        reply_service.add_message(mode.value)
