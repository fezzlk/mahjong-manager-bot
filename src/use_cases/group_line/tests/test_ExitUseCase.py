from DomainModel.entities.Group import Group, GroupMode
from use_cases.group_line.ExitUseCase import ExitUseCase
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import (
    group_repository,
    match_repository,
    hanchan_repository,
)
from linebot.models import TextSendMessage
from line_models.Event import Event
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match
from DomainModel.entities.Group import Group, GroupMode

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.input.value,
    _id=1,
)

dummy_match = Match(
    line_group_id=dummy_group.line_group_id,
    status=2,
    _id=1,
)

dummy_hanchan = Hanchan(
    line_group_id=dummy_group.line_group_id,
    match_id=1,
    status=2,
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


def test_fail_no_group():
        # Arrange
        use_case = ExitUseCase()
        request_info_service.set_req_info(event=dummy_event)

        # Act
        use_case.execute()

        # Assert
        assert len(reply_service.texts) == 1
        assert reply_service.texts[0].text == 'グループが登録されていません。招待し直してください。'


def test_execute():
    # Arrange
    use_case = ExitUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)

    # Act
    use_case.execute()

    # Assert
    result = group_repository.find()
    assert len(result) == 1
    assert result[0].line_group_id == dummy_group.line_group_id
    assert result[0].mode == 'wait'
    assert len(reply_service.texts) == 1
    assert isinstance(reply_service.texts[0], TextSendMessage)
    assert reply_service.texts[0].text == '始める時は「_start」と入力してください。'


def test_execute_with_active_hanchan():
    # Arrange
    use_case = ExitUseCase()
    request_info_service.set_req_info(event=dummy_event)
    hanchan_repository.create(dummy_hanchan)
    dummy_match.active_hanchan_id = dummy_hanchan._id
    match_repository.create(dummy_match)
    dummy_group.active_match_id = dummy_match._id
    group_repository.create(dummy_group)

    # Act
    use_case.execute()

    # Assert
    result = group_repository.find()
    assert len(result) == 1
    assert result[0].line_group_id == dummy_group.line_group_id
    assert result[0].mode == 'wait'
    assert result[0].active_match_id == dummy_match._id
    assert len(reply_service.texts) == 1
    assert isinstance(reply_service.texts[0], TextSendMessage)
    assert reply_service.texts[0].text == '始める時は「_start」と入力してください。'
    matches = match_repository.find()
    assert len(matches) == 1
    assert matches[0].active_hanchan_id is None
    assert matches[0].status == dummy_match.status
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 0