"""reply"""

from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction,
    MessageAction,
    URIAction,
)

import json


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

    def add_settings_menu(self, key=''):
        if key == '':
            self.services.config_service.reply()
            button = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='設定変更',
                    text='現在以下の項目のみ変更可能です。',
                    actions=[
                        PostbackAction(
                            label='レート',
                            display_text='レート',
                            data='_setting レート'
                        ),
                        PostbackAction(
                            label='飛び賞',
                            display_text='飛び賞',
                            data='_setting 飛び賞'
                        ),
                    ]
                )
            )
        elif key == 'レート':
            button = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='レート変更',
                    text='レートを選んでください',
                    actions=[
                        PostbackAction(
                            label=f'点{i}',
                            display_text=f'点{i}',
                            data=f'_update_config レート 点{i}'
                        ) for i in range(1, 4)
                    ] + [
                        PostbackAction(
                            label='点4~6',
                            display_text='点4~6',
                            data='_setting 高レート'
                        )
                    ]
                )
            )
        elif key == '高レート':
            button = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='レート変更',
                    text='レートを選んでください',
                    actions=[
                        PostbackAction(
                            label=f'点{i}',
                            display_text=f'点{i}',
                            data=f'_update_config レート 点{i}'
                        ) for i in range(4, 7)
                    ] + [
                        PostbackAction(
                            label='点1~3',
                            display_text='点1~3',
                            data='_setting レート'
                        )
                    ]
                )
            )
        elif key == '飛び賞':
            button = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='飛び賞変更',
                    text='いくらにしますか？',
                    actions=[
                        PostbackAction(
                            label=p,
                            display_text=p,
                            data=f'_update_config 飛び賞 {p}'
                        ) for p in [0, 10, 20, 30]
                    ]
                )
            )

        self.buttons.append(button)

    def add_tobi_menu(self, members):
        self.buttons.append(
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='飛び賞おめでとうございます',
                    text='どなたが飛ばしましたか？',
                    actions=[
                        PostbackAction(
                            label=member,
                            display_text=member,
                            data=f'_tobi {member}'
                        ) for member in members
                    ]
                )
            )
        )

    def add_submit_results_by_ocr_menu(self, results):
        self.buttons.append(
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='画像読み込み完了',
                    text=f'内容があっているか確認してください。',
                    actions=[
                        PostbackAction(
                            label='この結果で計算する',
                            display_text='この結果で計算する',
                            data='_add_result '+json.dumps(results),
                        ),
                        PostbackAction(
                            label='手入力する',
                            display_text='手入力する',
                            data='_input'
                        ),
                    ]
                )
            )
        )
