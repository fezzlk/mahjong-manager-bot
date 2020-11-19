from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction,
    MessageAction,
    URIAction,
)

class ReplyService:

    def __init__(self, services):
        self.services = services
        self.texts = []
        self.buttons = []

    def add_text(self, text):
        self.texts.append(text)

    def reply(self, event):
        if len(self.texts) == 0:
            return
        self.services.app_service.line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=text) for text in self.texts] + self.buttons)
        self.reset()

    def reset(self):
        self.texts = []
        self.buttons = []

    def add_start_menu(self):
        self.buttons.append(TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='スタートメニュー',
                text='Please select',
                actions=[
                    PostbackAction(
                        label='postback',
                        display_text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message',
                        text='message text'
                    ),
                    URIAction(
                        label='uri',
                        uri='https://github.com/line/line-bot-sdk-python'
                    )
                ]
            )
        )
    )