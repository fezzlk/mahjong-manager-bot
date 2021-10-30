from typing import Dict, List
from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ImageSendMessage,
    ButtonsTemplate,
    PostbackAction,
)

import json
from messaging_api_setting import line_bot_api
from .interfaces.IReplyService import IReplyService
from linebot.models.events import Event


class ReplyService(IReplyService):

    def __init__(self):
        self.texts = []
        self.buttons = []
        self.images = []

    def add_message(
        self,
        text: str,
    ) -> None:
        self.texts.append(TextSendMessage(text=text))

    def add_image(self, image_url: str) -> None:
        self.images.append(
            ImageSendMessage(
                original_content_url=image_url,
                preview_image_url=image_url,
            )
        )

    def add_start_menu(self) -> None:
        self.buttons.append(
            TemplateSendMessage(
                alt_text='Start Menu',
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

    def add_others_menu(self) -> None:
        self.buttons.append(
            TemplateSendMessage(
                alt_text='Other Menu',
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
                            label='設定',
                            display_text='設定',
                            data='_setting'
                        ),
                    ]
                )
            )
        )

    def add_settings_menu(self, key: str = '') -> None:
        if key == '':
            button = TemplateSendMessage(
                alt_text='Settings Menu',
                template=ButtonsTemplate(
                    title='設定',
                    text='変更したい項目を選んでください。',
                    actions=[
                        PostbackAction(
                            label='レート',
                            display_text='レート',
                            data='_setting レート'
                        ),
                        PostbackAction(
                            label='順位点',
                            display_text='順位点',
                            data='_setting 順位点'
                        ),
                        PostbackAction(
                            label='飛び賞',
                            display_text='飛び賞',
                            data='_setting 飛び賞'
                        ),
                        PostbackAction(
                            label='端数計算方法',
                            display_text='端数計算方法',
                            data='_setting 端数計算方法'
                        ),
                    ]
                )
            )
        elif key == 'レート':
            button = TemplateSendMessage(
                alt_text='Low Rate Setting',
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
                            label='点4~',
                            display_text='点4~',
                            data='_setting 高レート'
                        )
                    ]
                )
            )
        elif key == '高レート':
            button = TemplateSendMessage(
                alt_text='High Rate Setting',
                template=ButtonsTemplate(
                    title='レート変更',
                    text='レートを選んでください',
                    actions=[
                        PostbackAction(
                            label=f'点{i}',
                            display_text=f'点{i}',
                            data=f'_update_config レート 点{i}'
                        ) for i in [4, 5, 10]
                    ] + [
                        PostbackAction(
                            label='点1~3',
                            display_text='点1~3',
                            data='_setting レート'
                        )
                    ]
                )
            )
        elif key == '順位点':
            button = TemplateSendMessage(
                alt_text='Ranking Point Setting',
                template=ButtonsTemplate(
                    title='順位点変更',
                    text='いくらにしますか？',
                    actions=[
                        PostbackAction(
                            label=i,
                            display_text=i,
                            data=f'_update_config 順位点 {i}'
                        ) for i in [
                            ','.join(['20', '10', '-10', '-20']),
                            ','.join(['30', '10', '-10', '-30']),
                        ]
                    ]
                )
            )
        elif key == '飛び賞':
            button = TemplateSendMessage(
                alt_text='Tobi Bonus Setting',
                template=ButtonsTemplate(
                    title='飛び賞変更',
                    text='いくらにしますか？',
                    actions=[
                        PostbackAction(
                            label=i,
                            display_text=i,
                            data=f'_update_config 飛び賞 {i}'
                        ) for i in [0, 10, 20, 30]
                    ]
                )
            )

        elif key == '端数計算方法':
            button = TemplateSendMessage(
                alt_text='Calculate Method Setting1',
                template=ButtonsTemplate(
                    title='端数計算方法変更',
                    text='どれにしますか？',
                    actions=[
                        PostbackAction(
                            label=i,
                            display_text=i,
                            data=f'_update_config 端数計算方法 {i}'
                        )
                        for i in [
                            '3万点以下切り上げ/以上切り捨て',
                            '五捨六入',
                            '四捨五入',
                        ]
                    ] + [
                        PostbackAction(
                            label='その他',
                            display_text='その他',
                            data='_setting 端数計算方法2'
                        )
                    ]
                )
            )

        elif key == '端数計算方法2':
            button = TemplateSendMessage(
                alt_text='Calculate Method Setting2',
                template=ButtonsTemplate(
                    title='端数計算方法変更',
                    text='どれにしますか？',
                    actions=[
                        PostbackAction(
                            label=i,
                            display_text=i,
                            data=f'_update_config 端数計算方法 {i}'
                        ) for i in [
                            '切り捨て',
                            '切り上げ',
                        ]
                    ] + [
                        PostbackAction(
                            label='その他',
                            display_text='その他',
                            data='_setting 端数計算方法'
                        )
                    ]
                )
            )

        self.buttons.append(button)

    def add_tobi_menu(self, player_id_and_names: List[Dict[str, str]]) -> None:
        self.buttons.append(
            TemplateSendMessage(
                alt_text='Select Tobi Player Menu',
                template=ButtonsTemplate(
                    title='飛び賞おめでとうございます',
                    text='どなたが飛ばしましたか？',
                    actions=[
                        PostbackAction(
                            label=player_id_and_name['name'],
                            display_text=player_id_and_name['name'],
                            data='_tobi ' + player_id_and_name['id'],
                        ) for player_id_and_name in player_id_and_names
                    ] + [
                        PostbackAction(
                            label='誰も飛ばしていません',
                            display_text='勝手に飛びました',
                            data='_tobi'
                        )
                    ]
                )
            )
        )

    def add_submit_results_by_ocr_menu(self, results: Dict[str, int]) -> None:
        self.buttons.append(
            TemplateSendMessage(
                alt_text='Approve OCR result Menu',
                template=ButtonsTemplate(
                    title='画像読み込み完了',
                    text='内容があっているか確認してください。',
                    actions=[
                        PostbackAction(
                            label='この結果で計算する',
                            display_text='この結果で計算する',
                            data='_add_result ' + json.dumps(results),
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

    def reply(self, event: Event) -> None:
        contents = self.texts + self.buttons + self.images

        if (len(contents) == 0):
            return
        if hasattr(event, 'reply_token'):
            line_bot_api.reply_message(
                event.reply_token,
                contents,
            )
        self.reset()

    def reset(self) -> None:
        self.texts = []
        self.buttons = []
        self.images = []
