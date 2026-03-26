from application_service import reply_service


class StartHistoryFlowUseCase:
    def execute(self) -> None:
        reply_service.add_history_target_quick_reply()
