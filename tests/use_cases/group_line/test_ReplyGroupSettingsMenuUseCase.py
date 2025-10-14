from typing import Tuple

import pytest
from linebot.models import TemplateSendMessage

from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainModel.entities.GroupSetting import GroupSetting
from line_models.Event import Event
from repositories import group_setting_repository
from use_cases.group_line.ReplyGroupSettingsMenuUseCase import (
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
    ]
)
def case1(request) -> Tuple[int]:
    return request.param


def test_execute_(case1):
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyGroupSettingsMenuUseCase()

    # Act
    use_case.execute(case1)

    # Assert
    assert len(reply_service.texts) == 0
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateSendMessage)
