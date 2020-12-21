"""reply"""

from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction,
    MessageAction,
    URIAction,
)


class ReplyService:
    """reply service"""

    def __init__(self, services):
        self.services = services
        self.texts = []
        self.buttons = []

    def add_text(self, text):
        """add"""

        self.texts.append(text)

    def reply(self, event):
        if (len(self.texts) == 0) & (len(self.buttons) == 0):
            return
        print(event.reply_token)
        print(self.texts)
        self.services.app_service.line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=text) for text in self.texts] + self.buttons)
        self.reset()

    def reset(self):
        self.texts = []
        self.buttons = []

    def add_start_menu(self):
        self.buttons.append(
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='スタートメニュー',
                    text='何をしますか？',
                    actions=[
                        PostbackAction(
                            label='結果を入力',
                            display_text='結果を入力',
                            data='_input'
                        ),
                        PostbackAction(
                            label='結果を確認',
                            display_text='結果を確認',
                            data='_results'
                        ),
                        PostbackAction(
                            label='精算',
                            display_text='精算',
                            data='_finish'
                        ),
                        PostbackAction(
                            label='その他',
                            display_text='その他',
                            data='_others'
                        ),
                    ]
                )
            )
        )

    def add_others_menu(self):
        self.buttons.append(
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='その他のメニュー',
                    text='何をしますか？',
                    actions=[
                        PostbackAction(
                            label='対戦履歴',
                            display_text='対戦履歴',
                            data='_matches'
                        ),
                        PostbackAction(
                            label='設定変更',
                            display_text='設定変更',
                            data='_setting'
                        ),
                    ]
                )
            )
        )

    def add_settings_menu(self):
        self.buttons.append(
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='設定変更',
                    text='どの設定を変更をしますか？',
                    actions=[
                        PostbackAction(
                            label='レート',
                            display_text='レート',
                            data='_update_req:レート'
                        ),
                        PostbackAction(
                            label='順位点',
                            display_text='順位点',
                            data='_update_req:順位点'
                        ),
                        PostbackAction(
                            label='飛び賞',
                            display_text='飛び賞',
                            data='_update_req:飛び賞'
                        ),
                    ]
                )
            )
        )
