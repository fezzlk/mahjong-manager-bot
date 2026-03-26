from application_service import (
    reply_service,
)
from domain_model.entities.user import UserMode
from domain_service import (
    user_service,
)


class UserExitCommandUseCase:

    def execute(
        self,
        line_user_id: str,
    ) -> None:
        user_service.chmod(line_user_id, UserMode.wait)
        reply_service.add_message("処理を中断しました。")
