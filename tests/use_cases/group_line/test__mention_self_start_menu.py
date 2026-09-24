"""Botへのメンションでスタートメニューを再表示する機能のテスト。

- wait モードで、他のどの分岐にも一致しない場合のみBotへのメンションで
  スタートメニューが再表示される
- input モード中は、メンションされていても既存の点数入力処理が優先され
  スタートメニューは表示されない(進行中フローを中断しない)
"""
from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from line_models.event import Event
from repositories import group_repository
from routing_by_text_in_group_line import routing_by_text_in_group_line

LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"
USER_ID = "U0123456789abcdefghijklmnopqrstu1"


def _make_event(text: str, mention_self: bool) -> Event:
    return Event(
        type="message",
        source_type="group",
        user_id=USER_ID,
        group_id=LINE_GROUP_ID,
        message_type="text",
        text=text,
        mention_self=mention_self,
    )


def test_mention_self_in_wait_mode_shows_start_menu():
    """waitモードでBotへのメンション(コマンドではない文言)を送るとスタートメニューが返る。"""
    group_repository.create(
        Group(line_group_id=LINE_GROUP_ID, mode=GroupMode.wait.value, _id=1),
    )

    request_info_service.set_req_info(event=_make_event("@麻雀マネージャー", mention_self=True))
    routing_by_text_in_group_line()

    assert len(reply_service.buttons) == 1
    assert reply_service.buttons[0].alt_text == "スタートメニュー"

    groups = group_repository.find({"line_group_id": LINE_GROUP_ID})
    assert groups[0].mode == GroupMode.wait.value


def test_no_mention_self_in_wait_mode_stays_silent():
    """waitモードで通常のメンションなしテキストは(既存仕様どおり)何も返信しない。"""
    group_repository.create(
        Group(line_group_id=LINE_GROUP_ID, mode=GroupMode.wait.value, _id=1),
    )

    request_info_service.set_req_info(event=_make_event("こんにちは", mention_self=False))
    routing_by_text_in_group_line()

    assert len(reply_service.buttons) == 0
    assert len(reply_service.texts) == 0


def test_mention_self_in_input_mode_does_not_interrupt():
    """inputモード中はBotへのメンションが含まれていても既存の点数入力処理が優先される。"""
    group_repository.create(
        Group(
            line_group_id=LINE_GROUP_ID,
            mode=GroupMode.input.value,
            _id=1,
        ),
    )

    request_info_service.set_req_info(event=_make_event("35000", mention_self=True))
    routing_by_text_in_group_line()

    # スタートメニュー(ButtonsTemplate)は表示されない
    start_menu_shown = any(
        getattr(b, "alt_text", None) == "スタートメニュー" for b in reply_service.buttons
    )
    assert start_menu_shown is False

    # inputモードのままメンションによって中断されていない
    groups = group_repository.find({"line_group_id": LINE_GROUP_ID})
    assert groups[0].mode == GroupMode.input.value
