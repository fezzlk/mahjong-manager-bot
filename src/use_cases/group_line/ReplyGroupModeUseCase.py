from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainService import (
    group_service,
)


class ReplyGroupModeUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        mode = group_service.get_mode(line_group_id)
        if mode is None:
            reply_service.add_message(
                "トークルームが登録されていません。招待し直してください。",
            )
            return

        reply_service.add_message(mode)
