from Domains.Entities.User import UserMode
from Services import (
    user_service,
    reply_service,
)


class UserExitCommandUseCase:

    def execute(
        self,
        line_user_id: str,
    ) -> None:
        user_service.chmod(line_user_id, UserMode.wait)
        reply_service.add_message('処理を中断しました。')
