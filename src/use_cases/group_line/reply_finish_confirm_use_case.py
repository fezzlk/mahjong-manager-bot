from application_service import (
    reply_service,
)


class ReplyFinishConfirmUseCase:

    def execute(self) -> None:
        reply_service.add_confirm_finish_menu()
