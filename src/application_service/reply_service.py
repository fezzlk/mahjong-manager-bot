import json
import logging
import threading
from typing import Dict, List

from linebot.v3.messaging import (
    ButtonsTemplate,
    FlexBox,
    FlexBubble,
    FlexButton,
    FlexCarousel,
    FlexMessage,
    FlexText,
    ImageMessage,
    PostbackAction,
    PushMessageRequest,
    QuickReply,
    QuickReplyItem,
    ReplyMessageRequest,
    TemplateMessage,
    TextMessage,
)
from linebot.v3.messaging.exceptions import ApiException
from linebot.v3.webhooks import Event

import env_var
from domain_model.constants import ROUNDING_METHOD_LIST
from domain_model.entities.user import User
from messaging_api_setting import line_bot_api

from .interfaces.i_reply_service import IReplyService

logger = logging.getLogger(__name__)


class ReplyService(IReplyService):
    def __init__(self):
        self._local = threading.local()

    def _state(self):
        local = self._local
        if not hasattr(local, "initialized"):
            local.texts = []
            local.buttons = []
            local.images = []
            local.initialized = True
        return local

    @property
    def texts(self) -> List[TextMessage]:
        return self._state().texts

    @texts.setter
    def texts(self, value: List[TextMessage]):
        self._state().texts = value

    @property
    def buttons(self) -> List[TemplateMessage]:
        return self._state().buttons

    @buttons.setter
    def buttons(self, value: List[TemplateMessage]):
        self._state().buttons = value

    @property
    def images(self) -> List[ImageMessage]:
        return self._state().images

    @images.setter
    def images(self, value: List[ImageMessage]):
        self._state().images = value

    def add_message(
        self,
        text: str,
    ) -> None:
        self.texts.append(TextMessage(text=text))

    def add_image(self, image_url: str) -> None:
        self.images.append(
            ImageMessage(
                original_content_url=image_url,
                preview_image_url=image_url,
            ),
        )

    def add_start_menu(self) -> None:
        self.buttons.append(
            TemplateMessage(
                alt_text="スタートメニュー",
                template=ButtonsTemplate(
                    title="スタートメニュー",
                    text="何をしますか？",
                    actions=[
                        PostbackAction(
                            label="結果を入力",
                            display_text="結果を入力",
                            data="_input",
                        ),
                        PostbackAction(
                            label="精算",
                            display_text="精算",
                            data="_finish_confirm",
                        ),
                        PostbackAction(
                            label="設定",
                            display_text="設定",
                            data="_setting",
                        ),
                        PostbackAction(
                            label="その他",
                            display_text="その他",
                            data="_others",
                        ),
                    ],
                ),
            ),
        )

    def add_others_menu(self) -> None:
        self.buttons.append(
            TemplateMessage(
                alt_text="その他のメニュー",
                template=ButtonsTemplate(
                    title="その他のメニュー",
                    text="何をしますか？",
                    actions=[
                        PostbackAction(
                            label="途中経過を確認",
                            display_text="途中経過を確認",
                            data="_active_match",
                        ),
                        PostbackAction(
                            label="対戦履歴",
                            display_text="対戦履歴",
                            data="_matches",
                        ),
                        PostbackAction(
                            label="成績推移",
                            display_text="成績推移",
                            data="_history_start",
                        ),
                    ],
                ),
            ),
        )

    def add_settings_menu(self, key: str = "") -> None:
        if key in {"", "メニュー1"}:
            self.buttons.append(
                TemplateMessage(
                    alt_text="設定メニュー1",
                    template=ButtonsTemplate(
                        title="設定",
                        text="変更したい項目を選んでください。",
                        actions=[
                            PostbackAction(
                                label="レート",
                                display_text="レート",
                                data="_setting レート",
                            ),
                            PostbackAction(
                                label="順位点",
                                display_text="順位点",
                                data="_setting 順位点",
                            ),
                            PostbackAction(
                                label="チップ",
                                display_text="チップ",
                                data="_setting チップ",
                            ),
                            PostbackAction(
                                label="飛び賞、端数計算方法",
                                display_text="飛び賞、端数計算方法",
                                data="_setting メニュー2",
                            ),
                        ],
                    ),
                ),
            )
        if key == "メニュー2":
            self.buttons.append(
                TemplateMessage(
                    alt_text="設定メニュー2",
                    template=ButtonsTemplate(
                        title="設定",
                        text="変更したい項目を選んでください。",
                        actions=[
                            PostbackAction(
                                label="飛び賞",
                                display_text="飛び賞",
                                data="_setting 飛び賞",
                            ),
                            PostbackAction(
                                label="端数計算方法",
                                display_text="端数計算方法",
                                data="_setting 端数計算方法",
                            ),
                            PostbackAction(
                                label="レート、順位点、チップ",
                                display_text="レート、順位点、チップ",
                                data="_setting メニュー1",
                            ),
                        ],
                    ),
                ),
            )
        elif key == "レート":
            self.texts.append(
                TextMessage(
                    text="レートを選んでください",
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyItem(
                                action=PostbackAction(
                                    label="なし",
                                    display_text="なし",
                                    data="_update_config レート 0",
                                ),
                            ),
                        ]
                        + [
                            QuickReplyItem(
                                action=PostbackAction(
                                    label=f"点{i}",
                                    display_text=f"点{i}",
                                    data=f"_update_config レート {i}",
                                ),
                            )
                            for i in [1, 2, 3, 4, 5, 10]
                        ],
                    ),
                ),
            )
        elif key == "順位点":
            self.buttons.append(
                TemplateMessage(
                    alt_text="順位点設定",
                    template=ButtonsTemplate(
                        title="順位点変更",
                        text="いくらにしますか？",
                        actions=[
                            PostbackAction(
                                label="/".join(i),
                                display_text="/".join(i),
                                data=f"_update_config 順位点 {','.join(i)}",
                            )
                            for i in [
                                ["20", "10", "-10", "-20"],
                                ["30", "10", "-10", "-30"],
                            ]
                        ],
                    ),
                ),
            )
        elif key == "飛び賞":
            self.buttons.append(
                TemplateMessage(
                    alt_text="飛び賞設定",
                    template=ButtonsTemplate(
                        title="飛び賞変更",
                        text="いくらにしますか？",
                        actions=[
                            PostbackAction(
                                label=str(i),
                                display_text=str(i),
                                data=f"_update_config 飛び賞 {i}",
                            )
                            for i in [0, 10, 20, 30]
                        ],
                    ),
                ),
            )

        elif key == "端数計算方法":
            self.buttons.append(
                TemplateMessage(
                    alt_text="計算方法設定1",
                    template=ButtonsTemplate(
                        title="端数計算方法変更",
                        text="どれにしますか？",
                        actions=[
                            PostbackAction(
                                label=ROUNDING_METHOD_LIST[i],
                                display_text=ROUNDING_METHOD_LIST[i],
                                data=f"_update_config 端数計算方法 {i}",
                            )
                            for i in range(3)
                        ]
                        + [
                            PostbackAction(
                                label="その他",
                                display_text="その他",
                                data="_setting 端数計算方法2",
                            ),
                        ],
                    ),
                ),
            )

        elif key == "端数計算方法2":
            self.buttons.append(
                TemplateMessage(
                    alt_text="計算方法設定2",
                    template=ButtonsTemplate(
                        title="端数計算方法変更",
                        text="どれにしますか？",
                        actions=[
                            PostbackAction(
                                label=ROUNDING_METHOD_LIST[i],
                                display_text=ROUNDING_METHOD_LIST[i],
                                data=f"_update_config 端数計算方法 {i}",
                            )
                            for i in range(3, 5)
                        ]
                        + [
                            PostbackAction(
                                label="その他",
                                display_text="その他",
                                data="_setting 端数計算方法",
                            ),
                        ],
                    ),
                ),
            )
        elif key == "チップ":
            self.buttons.append(
                TemplateMessage(
                    alt_text="チップ設定",
                    template=ButtonsTemplate(
                        title="チップ",
                        text="どれにしますか？",
                        actions=[
                            PostbackAction(
                                label="なし",
                                display_text="なし",
                                data="_update_config チップ 0",
                            ),
                            PostbackAction(
                                label="あり(1枚=1点)",
                                display_text="あり(1枚=1点)",
                                data="_update_config チップ 1",
                            ),
                        ],
                    ),
                ),
            )

    def add_tobi_menu(self, player_id_and_names: List[Dict[str, str]]) -> None:
        self.buttons.append(
            TemplateMessage(
                alt_text="飛び賞プレイヤー選択",
                template=ButtonsTemplate(
                    title="飛び賞おめでとうございます",
                    text="どなたが飛ばしましたか？",
                    actions=[
                        PostbackAction(
                            label=player_id_and_name["name"],
                            display_text=player_id_and_name["name"],
                            data="_tobi " + player_id_and_name["_id"],
                        )
                        for player_id_and_name in player_id_and_names
                    ]
                    + [
                        PostbackAction(
                            label="誰も飛ばしていません",
                            display_text="勝手に飛びました",
                            data="_tobi",
                        ),
                    ],
                ),
            ),
        )

    def add_chip_complete_button(self) -> None:
        self.buttons.append(
            TemplateMessage(
                alt_text="チップ入力完了",
                template=ButtonsTemplate(
                    title="チップ入力",
                    text="各自のチップ増減数を入力してください。\n全員分の入力が完了したらボタンを押してください。",
                    actions=[
                        PostbackAction(
                            label="入力完了",
                            display_text="入力完了",
                            data="_chip_ok",
                        ),
                    ],
                ),
            ),
        )

    def add_submit_results_by_ocr_menu(self, results: Dict[str, int]) -> None:
        self.buttons.append(
            TemplateMessage(
                alt_text="画像読み込み実行",
                template=ButtonsTemplate(
                    title="画像読み込み完了",
                    text="内容があっているか確認してください。",
                    actions=[
                        PostbackAction(
                            label="この結果で計算する",
                            display_text="この結果で計算する",
                            data="_add_result " + json.dumps(results),
                        ),
                        PostbackAction(
                            label="手入力する",
                            display_text="手入力する",
                            data="_input",
                        ),
                    ],
                ),
            ),
        )

    def reply(self, event: Event) -> None:
        contents = self.texts + self.buttons + self.images

        if len(contents) == 0:
            return
        if hasattr(event, "reply_token"):
            try:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=contents,
                    ),
                )
            except ApiException as err:
                logger.warning("リプライに失敗しました: %s", err)
                # reply_token 期限切れ等の場合は push_message でフォールバック送信
                push_to = None
                if hasattr(event, "source"):
                    source = event.source
                    if hasattr(source, "group_id") and source.group_id:
                        push_to = source.group_id
                    elif hasattr(source, "user_id") and source.user_id:
                        push_to = source.user_id
                if push_to:
                    try:
                        text_contents = [m for m in contents if isinstance(m, TextMessage)]
                        if text_contents:
                            line_bot_api.push_message(
                                PushMessageRequest(
                                    to=push_to,
                                    messages=text_contents,
                                ),
                            )
                    except ApiException:
                        logger.exception("フォールバック push も失敗しました")
                self.push_a_message(
                    to=env_var.SERVER_ADMIN_LINE_USER_ID,
                    message=str(err),
                )

    def add_confirm_finish_menu(self) -> None:
        self.buttons.append(
            TemplateMessage(
                alt_text="精算実行確認",
                template=ButtonsTemplate(
                    title="精算",
                    text="本日の結果入力を終了し、総合結果を表示します。よろしいですか？",
                    actions=[
                        PostbackAction(
                            label="はい",
                            display_text="はい",
                            data="_finish",
                        ),
                        PostbackAction(
                            label="いいえ",
                            display_text="いいえ",
                            data="_start",
                        ),
                    ],
                ),
            ),
        )

    def add_history_target_quick_reply(self) -> None:
        self.texts.append(
            TextMessage(
                text="誰の成績推移を表示しますか？",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyItem(
                            action=PostbackAction(
                                label="自分だけ",
                                display_text="自分だけ",
                                data="_history_target?t=self",
                            ),
                        ),
                        QuickReplyItem(
                            action=PostbackAction(
                                label="グループ全員",
                                display_text="グループ全員",
                                data="_history_target?t=all",
                            ),
                        ),
                        QuickReplyItem(
                            action=PostbackAction(
                                label="ユーザを選ぶ",
                                display_text="ユーザを選ぶ",
                                data="_history_target?t=select",
                            ),
                        ),
                    ],
                ),
            ),
        )

    def add_personal_history_group_quick_reply(self, groups) -> None:
        items = [
            QuickReplyItem(
                action=PostbackAction(
                    label="全グループ",
                    display_text="全グループ",
                    data="_personal_history?g=all",
                ),
            )
        ]
        for g in groups[:12]:
            label = (g.group_name or g.line_group_id)[:20]
            items.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"_personal_history?g={g.line_group_id}",
                    ),
                )
            )
        self.texts.append(
            TextMessage(
                text="どのグループの成績を表示しますか？",
                quick_reply=QuickReply(items=items),
            )
        )

    def add_history_period_quick_reply(self) -> None:
        self.texts.append(
            TextMessage(
                text="期間を選んでください。",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyItem(
                            action=PostbackAction(
                                label="今月",
                                display_text="今月",
                                data="_history_exec?p=month",
                            ),
                        ),
                        QuickReplyItem(
                            action=PostbackAction(
                                label="先月",
                                display_text="先月",
                                data="_history_exec?p=last_month",
                            ),
                        ),
                        QuickReplyItem(
                            action=PostbackAction(
                                label="直近3ヶ月",
                                display_text="直近3ヶ月",
                                data="_history_exec?p=3months",
                            ),
                        ),
                        QuickReplyItem(
                            action=PostbackAction(
                                label="半年",
                                display_text="半年",
                                data="_history_exec?p=6months",
                            ),
                        ),
                        QuickReplyItem(
                            action=PostbackAction(
                                label="全期間",
                                display_text="全期間",
                                data="_history_exec?p=all",
                            ),
                        ),
                    ],
                ),
            ),
        )

    def add_history_user_select_carousel(
        self, members: List[User], selected_ids: List[str],
    ) -> None:
        bubbles = []
        for user in members:
            is_selected = user.line_user_id in selected_ids
            body_bg_color = "#1DB446" if is_selected else "#FFFFFF"
            btn_label = f"✓ {user.line_user_name}" if is_selected else user.line_user_name
            bubbles.append(
                FlexBubble(
                    body=FlexBox(
                        layout="vertical",
                        background_color=body_bg_color,
                        contents=[
                            FlexText(
                                text=user.line_user_name,
                                weight="bold",
                                size="md",
                                wrap=True,
                                color="#FFFFFF" if is_selected else "#333333",
                            ),
                        ],
                    ),
                    footer=FlexBox(
                        layout="vertical",
                        contents=[
                            FlexButton(
                                action=PostbackAction(
                                    label=btn_label[:20],
                                    display_text=btn_label[:20],
                                    data=f"_history_toggle?u={user.line_user_id}",
                                ),
                                style="primary" if is_selected else "secondary",
                            ),
                        ],
                    ),
                ),
            )

        # 確定 Bubble
        n = len(selected_ids)
        confirm_label = f"この{n}人で表示する" if n > 0 else "選択してください"
        bubbles.append(
            FlexBubble(
                body=FlexBox(
                    layout="vertical",
                    contents=[
                        FlexText(
                            text=f"{n}人選択中",
                            weight="bold",
                            size="lg",
                        ),
                    ],
                ),
                footer=FlexBox(
                    layout="vertical",
                    contents=[
                        FlexButton(
                            action=PostbackAction(
                                label=confirm_label,
                                display_text=confirm_label,
                                data="_history_confirm",
                            ),
                            style="primary",
                        ),
                    ],
                ),
            ),
        )

        self.buttons.append(
            FlexMessage(
                alt_text="ユーザを選んでください",
                contents=FlexCarousel(contents=bubbles),
            ),
        )

    def push_a_message(self, to: str, message: str) -> None:
        line_bot_api.push_message(
            PushMessageRequest(
                to=to,
                messages=[TextMessage(text=message)],
            ),
        )

    def reset(self) -> None:
        self.texts = []
        self.buttons = []
        self.images = []

    def create_and_reply_file_upload_error(self, title: str, sender: str) -> None:
        self.reset()
        self.add_message(text="システムエラーが発生しました。")
        messages = [
            f"{title}の画像アップロードに失敗しました",
            "送信者: " + sender,
        ]
        self.push_a_message(
            to=env_var.SERVER_ADMIN_LINE_USER_ID,
            message="\n".join(messages),
        )
