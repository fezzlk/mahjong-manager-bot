import pytest
from linebot.models import (
    TemplateSendMessage,
    TextSendMessage,
)

from ApplicationService import (
    reply_service,
    request_info_service,
)
from repositories import group_repository
from tests.dummies import (
    generate_dummy_join_event,
)
from use_cases.group_line.JoinGroupUseCase import JoinGroupUseCase


def test_fail_no_line_group_id():
    with pytest.raises(ValueError):
        # Arrange
        use_case = JoinGroupUseCase()

        # Act
        use_case.execute()

        # Assert


def test_execute():
    # Arrange
    dummy_event = generate_dummy_join_event()
    request_info_service.set_req_info(event=dummy_event)

    use_case = JoinGroupUseCase()

    # Act
    use_case.execute()

    # Assert
    result = group_repository.find()
    assert len(result) == 1
    assert result[0].line_group_id == dummy_event.source.group_id
    assert result[0].mode == "wait"
    assert len(reply_service.texts) == 3
    assert isinstance(reply_service.texts[0], TextSendMessage)
    assert isinstance(reply_service.texts[1], TextSendMessage)
    assert isinstance(reply_service.texts[2], TextSendMessage)
    assert reply_service.texts[0].text == "麻雀の成績管理Botです。参加者は友達登録してください。"
    assert reply_service.texts[1].text == "1半荘が終了したら下のメニューの「結果を入力」を押し、それぞれ素点を入力して下さい。"
    assert reply_service.texts[2].text == "レートや点数計算方法は「設定」で変更可能です。"
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateSendMessage)
