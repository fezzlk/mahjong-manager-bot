import env_var
from application_service import (
    reply_service,
)


class ReplyUrlUseCase:

    def execute(self) -> None:
        reply_service.add_message(
            env_var.SERVER_URL,
        )
