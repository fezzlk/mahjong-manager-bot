from DomainModel.entities.Group import Group, GroupMode
from use_cases.group_line.ReplyGroupModeUseCase import ReplyGroupModeUseCase
from ApplicationService import (
    request_info_service,
    reply_service,
)
from line_models.Event import Event
from repositories import group_repository

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.wait.value,
)

dummy_event = Event(
    type='message',
    source_type='group',
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type='text',
    text='dummy_text',
)


def test_execute():
    # Arrange
    group_repository.create(dummy_group)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyGroupModeUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == 'wait'
