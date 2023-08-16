from DomainModel.entities.Group import Group, GroupMode
from use_cases.group_line.GroupQuitUseCase import GroupQuitUseCase
from repositories import group_repository
from DomainModel.entities.Group import Group, GroupMode
from line_models.Event import Event
from ApplicationService import request_info_service


dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.input.value,
    _id=1,
)

dummy_event = Event(
    event_type='message',
    source_type='group',
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type='text',
    text='_exit',
)

def test_fail_no_line_group_id():
        # Arrange
        use_case = GroupQuitUseCase()
        group_repository.create(dummy_group)
        request_info_service.set_req_info(event=dummy_event)

        # Act
        use_case.execute()

        # Assert
        groups = group_repository.find()
        assert len(groups) == 0