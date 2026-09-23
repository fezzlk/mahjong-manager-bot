import logging
import threading
from typing import Dict, List, Tuple

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

    def add_message_with_exit_button(
        self,
        text: str,
    ) -> None:
        """入力・シミュレーション開始時のメッセージに、中断(_exit)ボタンを添える。"""
        label = "中断する"
        self.texts.append(
            TextMessage(
                text=text,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyItem(
                            action=PostbackAction(
                                label=label,
                                display_text=label,
                                data="_exit",
                            ),
                        ),
                    ],
                ),
            ),
        )

    def add_image(self, image_url: str, quick_reply=None) -> None:
        self.images.append(
            ImageMessage(
                original_content_url=image_url,
                preview_image_url=image_url,
                quick_reply=quick_reply,
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
                            label="対戦管理",
                            display_text="対戦管理",
                            data="_others",
                        ),
                        PostbackAction(
                            label="設定",
                            display_text="設定",
                            data="_setting",
                        ),
                    ],
                ),
            ),
        )

    def add_others_menu(self) -> None:
        """対戦管理メニュー(旧「その他」)。

        ButtonsTemplateの4件上限を超えるため、会話履歴に残るFlexCarouselで
        カテゴリ別のカードに並べる。
        """
        self._add_menu_carousel(
            alt_text="対戦管理メニュー",
            sections=[
                ("進行中の対戦", [
                    ("途中経過を確認", "_active_match"),
                    ("新しい対戦を始める", "_new_match"),
                    ("シミュレーション", "_sim"),
                ]),
                ("戦績", [
                    ("成績推移", "_history_start"),
                    ("対戦履歴", "_matches"),
                    ("累計得点表・順位表", "_ranking"),
                    ("個人の順位推移", "_rank"),
                    ("個人の順位分布", "_rank_detail"),
                ]),
            ],
        )

    def _add_menu_carousel(
        self,
        alt_text: str,
        sections: List[Tuple[str, List[Tuple[str, str]]]],
    ) -> None:
        """(カード見出し, [(ボタンラベル, postback data), ...]) の並びからメニュー用FlexCarouselを追加する。"""
        bubbles = []
        for title, items in sections:
            bubbles.append(
                FlexBubble(
                    body=FlexBox(
                        layout="vertical",
                        spacing="sm",
                        contents=[
                            FlexText(text=title, weight="bold", size="lg"),
                            *[
                                FlexButton(
                                    action=PostbackAction(
                                        label=label,
                                        display_text=label,
                                        data=data,
                                    ),
                                    style="secondary",
                                    height="sm",
                                )
                                for label, data in items
                            ],
                        ],
                    ),
                ),
            )
        self.buttons.append(
            FlexMessage(
                alt_text=alt_text,
                contents=FlexCarousel(contents=bubbles),
            ),
        )

    def add_settings_menu(self, key: str = "", num_of_players: int = 4) -> None:
        # メニュー1/メニュー2は旧ButtonsTemplate時代のページ切替キー。
        # 会話履歴に残った古いボタンから押された場合も同じカルーセルを返す。
        if key in {"", "メニュー1", "メニュー2"}:
            self._add_menu_carousel(
                alt_text="設定メニュー",
                sections=[
                    ("精算ルール", [
                        ("レート", "_setting レート"),
                        ("順位点", "_setting 順位点"),
                        ("チップ", "_setting チップ"),
                        ("飛び賞", "_setting 飛び賞"),
                        ("端数計算方法", "_setting 端数計算方法"),
                    ]),
                    ("メンバー", [
                        ("人数", "_setting 人数"),
                        ("ゲスト", "_setting ゲスト"),
                    ]),
                    ("その他", [
                        ("他グループへ統合", "_migrate"),
                        ("ヘルプ", "_help"),
                    ]),
                ],
            )
        elif key == "人数":
            self.texts.append(
                TextMessage(
                    text="何人麻雀にしますか？",
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyItem(
                                action=PostbackAction(
                                    label=f"{n}人",
                                    display_text=f"{n}人",
                                    data=f"_update_config 人数 {n}",
                                ),
                            )
                            for n in [4, 3]
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
                            # 順位点は人数分の要素数でないと更新時に弾かれるため、
                            # 現在の人数に合わせた選択肢を出す
                            for i in (
                                [["30", "0", "-30"], ["20", "0", "-20"]]
                                if num_of_players == 3
                                else [["20", "10", "-10", "-20"], ["30", "10", "-10", "-30"]]
                            )
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
            ),
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
                ),
            )
        self.texts.append(
            TextMessage(
                text="どのグループの成績を表示しますか？",
                quick_reply=QuickReply(items=items),
            ),
        )

    def add_migrate_target_quick_reply(self, groups) -> None:
        items = []
        for g in groups[:13]:
            label = (g.group_name or g.line_group_id)[:20]
            items.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"_migrate_confirm?to={g.line_group_id}",
                    ),
                ),
            )
        self.texts.append(
            TextMessage(
                text="どのグループに統合しますか？\n（このグループの成績が選択先グループに含まれます）",
                quick_reply=QuickReply(items=items),
            ),
        )

    def add_reopen_target_quick_reply(self, matches) -> None:
        items = []
        for m in matches[:13]:
            label = (m.name or str(m._id))[:20]
            items.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"_reopen_confirm?to={m._id}",
                    ),
                ),
            )
        self.texts.append(
            TextMessage(
                text="どの対戦を再オープンしますか？（直近10件の精算済み対戦）",
                quick_reply=QuickReply(items=items),
            ),
        )

    def add_match_target_quick_reply(self, matches, start_index: int) -> None:
        """対戦詳細選択用のQuick Replyを追加する。

        matchesは全件(古い順)のうち末尾10件相当を渡す想定。start_indexは
        全体リスト内でのmatches[0]の「第N回」番号(1始まり)。
        """
        items = []
        for i, m in enumerate(matches):
            label = f"第{start_index + i}回"
            items.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"_match_select?to={m._id}",
                    ),
                ),
            )
        # 対戦履歴一覧から複数の対戦をまとめて集計する入口(FEZ-234)
        items.append(
            QuickReplyItem(
                action=PostbackAction(
                    label="まとめて精算",
                    display_text="まとめて精算",
                    data="_sum_matches",
                ),
            ),
        )
        self.texts.append(
            TextMessage(
                text="どの対戦の詳細を見ますか？（直近10件）",
                quick_reply=QuickReply(items=items),
            ),
        )

    def add_sum_matches_select_quick_reply(self, matches, start_index: int, selected_match_ids) -> None:
        """対戦横断の合計集計(sum_matches)用の複数選択Quick Replyを追加する。

        matchesは全件(古い順)のうち末尾10件相当を渡す想定。start_indexは
        全体リスト内でのmatches[0]の「第N回」番号(1始まり)。トグルのたびに
        選択状態を反映してこのメソッドで再送信する。
        """
        items = []
        for i, m in enumerate(matches):
            is_selected = str(m._id) in selected_match_ids
            label = f"✓第{start_index + i}回" if is_selected else f"第{start_index + i}回"
            items.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"_sum_matches_toggle?to={m._id}",
                    ),
                ),
            )
        items.append(
            QuickReplyItem(
                action=PostbackAction(
                    label=f"合計を見る({len(selected_match_ids)}件選択中)",
                    display_text="合計を見る",
                    data="_sum_matches_confirm",
                ),
            ),
        )
        self.texts.append(
            TextMessage(
                text="対戦をタップして選択/解除できます。選び終わったら「合計を見る」を押してください。",
                quick_reply=QuickReply(items=items),
            ),
        )

    def build_match_detail_quick_reply(self, match) -> QuickReply:
        """対戦詳細画面に付けるボタン(対戦の削除・再オープン)のQuick Replyを返す。

        戻り値は呼び出し元が最後に送信されるメッセージ(画像)に渡すこと
        (build_drop_target_quick_reply参照)。
        """
        return QuickReply(
            items=[
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"{command}?to={match._id}",
                    ),
                )
                for label, command in [
                    ("この対戦を再オープン", "_reopen_confirm"),
                    ("この対戦を削除", "_drop_m_select"),
                ]
            ],
        )

    def build_drop_target_quick_reply(self, hanchans, start_index: int) -> QuickReply:
        """半荘削除選択用のQuick Replyを構築して返す。

        hanchansは対象対戦の全アーカイブ済み半荘(古い順)のうち末尾10件相当を
        渡す想定。start_indexは全体リスト内でのhanchans[0]の「第N回」番号(1始まり)。

        戻り値は呼び出し元がadd_image(quick_reply=...)等、実際に送信される
        メッセージ列の最後の1件に渡すこと。reply()はtexts+buttons+imagesの
        順で連結して送信するため、途中のテキストにQuick Replyを付けても
        LINE側では最後のメッセージのQuick Replyしか表示されない。
        """
        items = []
        for i, h in enumerate(hanchans):
            label = f"第{start_index + i}回を削除"
            items.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"_drop_select?to={h._id}",
                    ),
                ),
            )
        return QuickReply(items=items)

    def add_input_target_quick_reply(self, matches) -> None:
        items = []
        for m in matches[:12]:
            label = (m.name or str(m._id))[:20]
            items.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"_input_select?to={m._id}",
                    ),
                ),
            )
        items.append(
            QuickReplyItem(
                action=PostbackAction(
                    label="新しい対戦を始める",
                    display_text="新しい対戦を始める",
                    data="_new_match",
                ),
            ),
        )
        self.texts.append(
            TextMessage(
                text="どの対戦の入力を始めますか？",
                quick_reply=QuickReply(items=items),
            ),
        )

    def add_new_match_confirm_menu(self, settings) -> None:
        # LINE ButtonsTemplateのtextは60文字程度が上限のため、詳細設定は
        # 「_setting」で別途確認できる前提で簡潔な文言に留める。
        chip_display = "なし" if settings.chip_rate == 0 else "あり"
        text = f"現在の設定(点{settings.rate}/チップ{chip_display})で新しい対戦を始めます。"
        self.buttons.append(
            TemplateMessage(
                alt_text="新しい対戦の開始確認",
                template=ButtonsTemplate(
                    title="新しい対戦",
                    text=text,
                    actions=[
                        PostbackAction(
                            label="作成する",
                            display_text="作成する",
                            data="_new_match_confirm",
                        ),
                    ],
                ),
            ),
        )

    def add_finish_target_quick_reply(self, matches) -> None:
        items = []
        for m in matches[:13]:
            label = (m.name or str(m._id))[:20]
            items.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"_finish_select?to={m._id}",
                    ),
                ),
            )
        self.texts.append(
            TextMessage(
                text="どの対戦を精算しますか？",
                quick_reply=QuickReply(items=items),
            ),
        )

    def add_active_match_target_quick_reply(self, matches) -> None:
        items = []
        for m in matches[:13]:
            label = (m.name or str(m._id))[:20]
            items.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"_active_match_select?to={m._id}",
                    ),
                ),
            )
        self.texts.append(
            TextMessage(
                text="どの対戦の途中経過を確認しますか？",
                quick_reply=QuickReply(items=items),
            ),
        )

    def add_guest_menu(self, guests) -> None:
        if guests:
            names = "\n".join(f"ゲスト{g.guest_number}" for g in guests)
            text = f"登録済みのゲスト:\n{names}"
        else:
            text = "登録済みのゲストはいません。"

        actions = [
            PostbackAction(
                label="追加",
                display_text="ゲストを追加",
                data="_guest_add",
            ),
        ]
        if guests:
            actions.append(
                PostbackAction(
                    label="削除",
                    display_text="ゲストを削除",
                    data="_setting ゲスト削除",
                ),
            )

        self.buttons.append(
            TemplateMessage(
                alt_text="ゲスト管理",
                template=ButtonsTemplate(
                    title="ゲスト管理",
                    text=text,
                    actions=actions,
                ),
            ),
        )

    def add_guest_remove_quick_reply(self, guests) -> None:
        if not guests:
            self.texts.append(TextMessage(text="削除できるゲストがいません。"))
            return

        items = []
        for g in guests[:13]:
            label = f"ゲスト{g.guest_number}"
            items.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"_guest_remove_confirm?number={g.guest_number}",
                    ),
                ),
            )
        self.texts.append(
            TextMessage(
                text="削除するゲストを選んでください。",
                quick_reply=QuickReply(items=items),
            ),
        )

    def add_personal_migrate_source_quick_reply(self, groups) -> None:
        """個人DM: 統合元 (旧グループ) 選択 QR"""
        items = []
        for g in groups[:13]:
            label = (g.group_name or g.line_group_id)[:20]
            items.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"_personal_migrate?src={g.line_group_id}",
                    ),
                ),
            )
        self.texts.append(
            TextMessage(
                text="どのグループを統合しますか？\n（成績を別グループに移したいグループを選んでください）",
                quick_reply=QuickReply(items=items),
            ),
        )

    def add_personal_migrate_dest_quick_reply(self, groups, src_group_id: str) -> None:
        """個人DM: 統合先 (新グループ) 選択 QR"""
        items = []
        for g in groups[:13]:
            label = (g.group_name or g.line_group_id)[:20]
            items.append(
                QuickReplyItem(
                    action=PostbackAction(
                        label=label,
                        display_text=label,
                        data=f"_personal_migrate?src={src_group_id}&to={g.line_group_id}",
                    ),
                ),
            )
        self.texts.append(
            TextMessage(
                text="どのグループに統合しますか？\n（選択先グループに成績がまとめられます）",
                quick_reply=QuickReply(items=items),
            ),
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
