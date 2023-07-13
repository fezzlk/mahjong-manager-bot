from DomainModel.entities.Group import Group, GroupMode
from tests.dummies import (
    generate_dummy_join_event,
)
from use_cases.group_line.GroupQuitUseCase import GroupQuitUseCase
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import group_repository
from linebot.models import TextSendMessage
import pytest
from line_models.Event import Event


def test_fail_no_line_group_id():
    with pytest.raises(ValueError):
        # Arrange
        use_case = GroupQuitUseCase()

        # Act
        use_case.execute()

        # Assert


dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.input.value,
)

dummy_event = Event(
    event_type='message',
    source_type='group',
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type='text',
    text='_exit',
)


def test_execute():
    # Arrange
    group_repository.create(dummy_group)
    dummy_event = generate_dummy_join_event()
    request_info_service.set_req_info(event=dummy_event)

    use_case = GroupQuitUseCase()

    # Act
    use_case.execute()

    # Assert
    result = group_repository.find()
    assert len(result) == 1
    assert result[0].line_group_id == dummy_event.source.group_id
    assert result[0].mode == 'wait'
    assert len(reply_service.texts) == 1
    assert isinstance(reply_service.texts[0], TextSendMessage)
    assert reply_service.texts[0].text == '始める時は「_start」と入力してください。'
