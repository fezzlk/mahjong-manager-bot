from use_cases.group_line.DisableMatchUseCase import DisableMatchUseCase
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import (
    match_repository,
    hanchan_repository,
)
from linebot.models import TextSendMessage
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
        status=1,
        _id=1,
    )
]


def test_execute():
    # Arrange
    use_case = DisableMatchUseCase()
    request_info_service.set_req_info(event=dummy_event)
    match_repository.create(dummy_matches[0])
    hanchan_repository.create(dummy_hanchans[0])

    # Act
    use_case.execute()

    # Assert
    match = match_repository.find()
    assert match[0].status == 0
    hanchan = hanchan_repository.find()
    assert hanchan[0].status == 0
    assert len(reply_service.texts) == 1
    assert isinstance(reply_service.texts[0], TextSendMessage)
    assert reply_service.texts[0].text == '対戦ID=1の結果を削除しました。'
