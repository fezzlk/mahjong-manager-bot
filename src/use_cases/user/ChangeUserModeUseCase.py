from domains.User import UserMode
from services import (
    user_service,
    reply_service,
)


class ChangeUserModeUseCase:

    def execute(
        self,
        line_user_id: str,
        mode: UserMode,
    ) -> None:
        user_service.chmod(line_user_id, mode)
        reply_service.add_message('処理を中断しました。')
        