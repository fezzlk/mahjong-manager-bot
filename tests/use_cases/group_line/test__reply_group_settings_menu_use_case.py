from typing import Tuple

import pytest
from linebot.models import TemplateSendMessage

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group_setting import GroupSetting
from line_models.event import Event
from repositories import group_setting_repository
from use_cases.group_line.reply_group_settings_menu_use_case import (
    ReplyGroupSettingsMenuUseCase,
)

dummy_group_settings = GroupSetting(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    rate=3,
    ranking_prize=[20, 10, -10, -20],
    chip_rate=1,
    tobi_prize=10,
    num_of_players=4,
    rounding_method=0,
    _id=1,
)

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
    # DB操作: group_setting_repository.create(dummy_group_settings)
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyGroupSettingsMenuUseCase()
    group_setting_repository.create(dummy_group_settings)

    # Act
    use_case.execute("")

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "[設定]\n4人麻雀\nレート: 点3\n順位点: 1着20/2着10/3着-10/4着-20\n飛び賞: 10点\nチップ: 1枚1点\n計算方法: 3万点以下切り上げ/以上切り捨て"
    )
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateSendMessage)


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
        == "[設定]\n4人麻雀\nレート: 点0\n順位点: 1着20/2着10/3着-10/4着-20\n飛び賞: 10点\nチップ: 1枚0点\n計算方法: 五捨六入"
    )
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateSendMessage)


@pytest.fixture(
    params=[
        ("メニュー2"),
        ("レート"),
        ("高レート"),
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
    # 目的: test_execute_ の挙動を検証する。
    # 入力: case1
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 0 件 / reply_service.buttons の件数が 1 件 / reply_service.buttons[0] が TemplateSendMessage 型
    # reply_service: buttons, texts
    # DB操作: なし
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyGroupSettingsMenuUseCase()

    # Act
    use_case.execute(case1)

    # Assert
    assert len(reply_service.texts) == 0
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateSendMessage)
