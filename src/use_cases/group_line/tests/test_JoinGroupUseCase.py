from tests.dummies import (
    generate_dummy_join_event,
)
from use_cases.group_line.JoinGroupUseCase import JoinGroupUseCase
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import group_repository
from linebot.models import TextSendMessage
import pytest


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
    assert result[0].mode == 'wait'
    assert len(reply_service.texts) == 1
    assert isinstance(reply_service.texts[0], TextSendMessage)
    assert reply_service.texts[0].text == 'こんにちは、今日は麻雀日和ですね。'
