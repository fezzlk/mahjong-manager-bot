from services import reply_service


class ReplyUseCases:
    """reply use cases"""

    def add_start_menu(self):
        reply_service.add_start_menu()

    def add_others_menu(self):
        reply_service.add_others_menu()
