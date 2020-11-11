from linebot.models import (
    TextSendMessage,
)

class ReplyService:

    def __init__(self, services):
        self.services = services
        self.replies = []

    def add(self, text):
        self.replies.append(text)

    def reply(self, event):
        if len(self.replies) == 0:
            return
        self.services.app_service.line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=reply) for reply in self.replies])
        self.reset()

    def reset(self):
        self.replies = []