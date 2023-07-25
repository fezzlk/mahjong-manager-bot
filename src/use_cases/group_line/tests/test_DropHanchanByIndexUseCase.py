from use_cases.group_line.DropHanchanByIndexUseCase import DropHanchanByIndexUseCase
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import (
    match_repository,
    hanchan_repository,
)
from line_models.Event import Event
from DomainModel.entities.Match import Match
from DomainModel.entities.Hanchan import Hanchan


dummy_event = Event(
    event_type='message',
    source_type='group',
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type='text',
    text='dummy_text',
)

dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        _id=1,
    ),
]
dummy_hanchans = [
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        status=2,
        _id=1,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        status=2,
        _id=2,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        status=2,
        _id=3,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        status=1,
        _id=4,
    ),
]


def test_execute():
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute(2)

    # Assert
    hanchan = hanchan_repository.find({'_id': 2})
    assert hanchan[0].status == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '半荘ID=2の結果を削除しました。'
