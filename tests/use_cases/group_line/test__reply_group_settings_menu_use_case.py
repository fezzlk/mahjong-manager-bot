from typing import Tuple

import pytest
from linebot.v3.messaging import TemplateMessage

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.group_setting import EmbeddedGroupSettings
from line_models.event import Event
from repositories import group_repository
from use_cases.group_line.reply_group_settings_menu_use_case import (
    ReplyGroupSettingsMenuUseCase,
)

dummy_line_group_id = "G0123456789abcdefghijklmnopqrstu1"

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="dummy_text",
)


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / reply_service.buttons の件数が 1 件 / reply_service.buttons[0] が TemplateSendMessage 型
    # reply_service: buttons, texts
    # DB操作: group_repository.create; group_repository.update_settings
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyGroupSettingsMenuUseCase()
    group_repository.create(Group(line_group_id=dummy_line_group_id, mode=GroupMode.wait.value))
    group_repository.update_settings(
        dummy_line_group_id,
        EmbeddedGroupSettings(rate=3, ranking_prize=[20, 10, -10, -20], chip_rate=1, tobi_prize=10, num_of_players=4, rounding_method=0),
    )

    # Act
    use_case.execute("")

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "[設定]\n4人麻雀\nレート: 点3\n順位点: 1着20/2着10/3着-10/4着-20\n飛び賞: 10点\nチップ: あり(1枚=1点)\n計算方法: 3万点以下切り上げ/以上切り捨て\n単位: pt"
    )
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateMessage)


def test_execute_no_settings():
    # 目的: test_execute_no_settings の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / reply_service.buttons の件数が 1 件 / reply_service.buttons[0] が TemplateSendMessage 型
    # reply_service: buttons, texts
    # DB操作: なし
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyGroupSettingsMenuUseCase()

    # Act
    use_case.execute("")

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "[設定]\n4人麻雀\nレート: 点0\n順位点: 1着20/2着10/3着-10/4着-20\n飛び賞: 10点\nチップ: なし\n計算方法: 五捨六入\n単位: pt"
    )
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateMessage)


@pytest.fixture(
    params=[
        ("メニュー2"),
        ("順位点"),
        ("飛び賞"),
        ("端数計算方法"),
        ("端数計算方法2"),
        ("チップ"),
    ],
)
def case1(request) -> Tuple[int]:
    return request.param


def test_execute_(case1):
    # 目的: ButtonsTemplate で返る設定メニューの挙動を検証する。
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyGroupSettingsMenuUseCase()

    # Act
    use_case.execute(case1)

    # Assert
    assert len(reply_service.texts) == 0
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateMessage)


def test_execute_rate():
    """レート設定は Quick Reply で返る。"""
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyGroupSettingsMenuUseCase()

    use_case.execute("レート")

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].quick_reply is not None
    assert len(reply_service.buttons) == 0
