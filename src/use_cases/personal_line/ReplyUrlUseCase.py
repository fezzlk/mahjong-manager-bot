from ApplicationService import (
    reply_service,
)
import env_var


class ReplyUrlUseCase:

    def execute(self) -> None:
        reply_service.add_message(
            env_var.SERVER_URL
        )
