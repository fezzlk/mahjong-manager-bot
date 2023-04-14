from DomainService import (
    user_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)


class ReplyUserModeUseCase:

    def execute(self) -> None:
        line_user_id = request_info_service.req_line_user_id
        mode = user_service.get_mode(line_user_id)
        if mode is None:
            reply_service.add_message(
                'ユーザーを認識できませんでした。当アカウントを一度ブロックし、ブロック解除してください。'
            )
            return
        reply_service.add_message(mode)
