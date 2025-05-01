import env_var
from ApplicationService import (
    reply_service,
)


class ReplyUrlUseCase:

    def execute(self) -> None:
        reply_service.add_message(
            env_var.SERVER_URL,
        )
