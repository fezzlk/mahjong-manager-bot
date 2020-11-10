from linebot.models import (
    TextSendMessage,
)

class ReplyService:

    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.replies = []

    def add(self, text):
        self.replies.append(text)

    def reply(self, event):
        self.line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=reply) for reply in self.replies])

    def reset(self):
        self.replies = []