from ctypes import Union
from typing import Dict, List
from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ImageSendMessage,
    ButtonsTemplate,
    PostbackAction,
)
import env_var

import json
from messaging_api_setting import line_bot_api
from .interfaces.IReplyService import IReplyService
from linebot.models.events import Event
from linebot.exceptions import LineBotApiError
from DomainModel.entities.GroupSetting import ROUNDING_METHOD_LIST


class ReplyService(IReplyService):

    def __init__(self):
        self.texts: List[TextSendMessage] = []
        self.buttons: List[Union[TemplateSendMessage, ButtonsTemplate]] = []
        self.images: List[ImageSendMessage] = []

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
                alt_text='スタートメニュー',
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
                            label='精算',
                            display_text='精算',
                            data='_finish_confirm'
                        ),
                        PostbackAction(
                            label='設定',
                            display_text='設定',
                            data='_setting'
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
                alt_text='その他のメニュー',
                template=ButtonsTemplate(
                    title='その他のメニュー',
                    text='何をしますか？',
                    actions=[
                        PostbackAction(
                            label='途中経過を確認',
                            display_text='途中経過を確認',
                            data='_active_match'
                        ),
                        PostbackAction(
                            label='対戦履歴',
                            display_text='対戦履歴',
                            data='_matches'
                        ),
                    ]
                )
            )
        )

    def add_settings_menu(self, key: str = '') -> None:
        if key == '' or key == 'メニュー1':
            self.buttons.append(TemplateSendMessage(
                alt_text='設定メニュー1',
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
                            label='チップ',
                            display_text='チップ',
                            data='_setting チップ'
                        ),
                        PostbackAction(
                            label='飛び賞、端数計算方法',
                            display_text='飛び賞、端数計算方法',
                            data='_setting メニュー2'
                        ),
                    ]
                )
            ))
        if key == 'メニュー2':
            self.buttons.append(TemplateSendMessage(
                alt_text='設定メニュー2',
                template=ButtonsTemplate(
                    title='設定',
                    text='変更したい項目を選んでください。',
                    actions=[
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
                        PostbackAction(
                            label='レート、順位点、チップ',
                            display_text='レート、順位点、チップ',
                            data='_setting メニュー1'
                        ),
                    ]
                )
            ))
        elif key == 'レート':
            self.buttons.append(TemplateSendMessage(
                alt_text='レート設定',
                template=ButtonsTemplate(
                    title='レート変更',
                    text='レートを選んでください',
                    actions=[
                        PostbackAction(
                            label=f'点{i}',
                            display_text=f'点{i}',
                            data=f'_update_config レート {i}'
                        ) for i in range(1, 4)
                    ] + [
                        PostbackAction(
                            label='点4~',
                            display_text='点4~',
                            data='_setting 高レート'
                        )
                    ]
                )
            ))
        elif key == '高レート':
            self.buttons.append(TemplateSendMessage(
                alt_text='高レート設定',
                template=ButtonsTemplate(
                    title='レート変更',
                    text='レートを選んでください',
                    actions=[
                        PostbackAction(
                            label=f'点{i}',
                            display_text=f'点{i}',
                            data=f'_update_config レート {i}'
                        ) for i in [4, 5, 10]
                    ] + [
                        PostbackAction(
                            label='点1~3',
                            display_text='点1~3',
                            data='_setting レート'
                        )
                    ]
                )
            ))
        elif key == '順位点':
            self.buttons.append(TemplateSendMessage(
                alt_text='順位点設定',
                template=ButtonsTemplate(
                    title='順位点変更',
                    text='いくらにしますか？',
                    actions=[
                        PostbackAction(
                            label='/'.join(i),
                            display_text='/'.join(i),
                            data=f"_update_config 順位点 {','.join(i)}"
                        ) for i in [
                            ['20', '10', '-10', '-20'],
                            ['30', '10', '-10', '-30'],
                        ]
                    ]
                )
            ))
        elif key == '飛び賞':
            self.buttons.append(TemplateSendMessage(
                alt_text='飛び賞設定',
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
            ))

        elif key == '端数計算方法':
            self.buttons.append(TemplateSendMessage(
                alt_text='計算方法設定1',
                template=ButtonsTemplate(
                    title='端数計算方法変更',
                    text='どれにしますか？',
                    actions=[
                        PostbackAction(
                            label=ROUNDING_METHOD_LIST[i],
                            display_text=ROUNDING_METHOD_LIST[i],
                            data=f'_update_config 端数計算方法 {i}'
                        )
                        for i in range(3)
                    ] + [
                        PostbackAction(
                            label='その他',
                            display_text='その他',
                            data='_setting 端数計算方法2'
                        )
                    ]
                )
            ))

        elif key == '端数計算方法2':
            self.buttons.append(TemplateSendMessage(
                alt_text='計算方法設定2',
                template=ButtonsTemplate(
                    title='端数計算方法変更',
                    text='どれにしますか？',
                    actions=[
                        PostbackAction(
                            label=ROUNDING_METHOD_LIST[i],
                            display_text=ROUNDING_METHOD_LIST[i],
                            data=f'_update_config 端数計算方法 {i}'
                        ) for i in range(3, 5)
                    ] + [
                        PostbackAction(
                            label='その他',
                            display_text='その他',
                            data='_setting 端数計算方法'
                        )
                    ]
                )
            ))
        elif key == 'チップ':
            self.buttons.append(TemplateSendMessage(
                alt_text='チップ設定',
                template=ButtonsTemplate(
                    title='チップ',
                    text='どれにしますか？',
                    actions=[
                        PostbackAction(
                            label=f'1枚{i}円',
                            display_text=f'1枚{i}円',
                            data=f'_update_config チップ {i}'
                        ) for i in [0, 10, 30]
                    ] + [
                        PostbackAction(
                            label='1枚50円以上',
                            display_text='1枚50円以上',
                            data='_setting 高チップ'
                        )
                    ]
                )
            ))
        elif key == '高チップ':
            self.buttons.append(TemplateSendMessage(
                alt_text='高チップ設定',
                template=ButtonsTemplate(
                    title='チップ',
                    text='どれにしますか？',
                    actions=[
                        PostbackAction(
                            label=f'1枚{i}円',
                            display_text=f'1枚{i}円',
                            data=f'_update_config チップ {i}'
                        ) for i in [50, 100, 500]
                    ] + [
                        PostbackAction(
                            label='1枚30円以下',
                            display_text='1枚30円以下',
                            data='_setting チップ'
                        )
                    ]
                )
            ))

    def add_tobi_menu(self, player_id_and_names: List[Dict[str, str]]) -> None:
        self.buttons.append(
            TemplateSendMessage(
                alt_text='飛び賞プレイヤー選択',
                template=ButtonsTemplate(
                    title='飛び賞おめでとうございます',
                    text='どなたが飛ばしましたか？',
                    actions=[
                        PostbackAction(
                            label=player_id_and_name['name'],
                            display_text=player_id_and_name['name'],
                            data='_tobi ' + player_id_and_name['_id'],
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
                alt_text='画像読み込み実行',
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
            try:
                line_bot_api.reply_message(
                    event.reply_token,
                    contents,
                )
            except LineBotApiError as err:
                print('リプライに失敗しました。')
                # contents の内容が原因でリプライが失敗した時のためのハンドリング
                line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage(text='システムエラーが発生しました。')],
                )
                self.push_a_message(
                    to=env_var.SERVER_ADMIN_LINE_USER_ID,
                    message=str(err),
                )

    def confirm_finish(self) -> None:
        self.buttons.append(
            TemplateSendMessage(
                alt_text='精算実行確認',
                template=ButtonsTemplate(
                    title='精算',
                    text='本日の結果入力を終了し、総合結果を表示します。よろしいですか？',
                    actions=[
                        PostbackAction(
                            label='はい',
                            display_text='はい',
                            data='_finish'
                        ),
                        PostbackAction(
                            label='いいえ',
                            display_text='いいえ',
                            data='_start'
                        ),
                    ]
                )
            )
        )

    def push_a_message(self, to: str, message: str) -> None:
        line_bot_api.push_message(to, [TextSendMessage(text=message)])

    def reset(self) -> None:
        self.texts = []
        self.buttons = []
        self.images = []

    def create_and_reply_file_upload_error(self, title: str, sender: str) -> None:
        self.reset()
        self.add_message(text='システムエラーが発生しました。')
        messages = [
            f'{title}の画像アップロードに失敗しました',
            '送信者: ' + sender,
        ]
        self.push_a_message(
            to=env_var.SERVER_ADMIN_LINE_USER_ID,
            message='\n'.join(messages),
        )