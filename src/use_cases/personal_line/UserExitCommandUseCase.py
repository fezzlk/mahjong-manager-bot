from ApplicationService import (
    reply_service,
)
from DomainModel.entities.User import UserMode
from DomainService import (
    user_service,
)


class UserExitCommandUseCase:

    def execute(
        self,
        line_user_id: str,
    ) -> None:
        user_service.chmod(line_user_id, UserMode.wait)
        reply_service.add_message("処理を中断しました。")
