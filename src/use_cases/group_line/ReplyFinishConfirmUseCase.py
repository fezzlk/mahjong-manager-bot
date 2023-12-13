from ApplicationService import (
    reply_service,
)


class ReplyFinishConfirmUseCase:

    def execute(self) -> None:
        reply_service.add_confirm_finish_menu()
