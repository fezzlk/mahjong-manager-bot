from Services import (
    reply_service,
)


class ReplyOthersMenuUseCase:

    def execute(self) -> None:
        reply_service.add_others_menu()
