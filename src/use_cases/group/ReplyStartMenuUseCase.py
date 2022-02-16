from Services import (
    reply_service,
)


class ReplyStartMenuUseCase:

    def execute(self) -> None:
        reply_service.add_start_menu()
