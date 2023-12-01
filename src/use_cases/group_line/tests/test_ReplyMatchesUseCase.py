from DomainModel.entities.Match import Match
from use_cases.group_line.ReplyMatchesUseCase import ReplyMatchesUseCase
from ApplicationService import (
    request_info_service,
    reply_service,
)
from line_models.Event import Event
from repositories import (
    match_repository,
)
from datetime import datetime

dummy_matches = [
    Match(
        _id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        created_at=datetime(2010, 1, 1, 1, 1, 1),
        sum_prices_with_tip={
            "U0123456789abcdefghijklmnopqrstu1": 1000,
            "U0123456789abcdefghijklmnopqrstu2": 1800,
            "U0123456789abcdefghijklmnopqrstu3": -1800,
            "U0123456789abcdefghijklmnopqrstu4": -400,
            "U0123456789abcdefghijklmnopqrstu5": -300,
            "dummy": -300,
        },
    ),
    Match(
        _id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        sum_scores={
            "U0123456789abcdefghijklmnopqrstu1": 30,
            "U0123456789abcdefghijklmnopqrstu2": 60,
            "U0123456789abcdefghijklmnopqrstu3": -60,
            "U0123456789abcdefghijklmnopqrstu4": -10,
            "U0123456789abcdefghijklmnopqrstu5": -10,
            "dummy": -10,
        },
        sum_prices={
            "U0123456789abcdefghijklmnopqrstu1": 900,
            "U0123456789abcdefghijklmnopqrstu2": 1800,
            "U0123456789abcdefghijklmnopqrstu3": -1800,
            "U0123456789abcdefghijklmnopqrstu4": -300,
            "U0123456789abcdefghijklmnopqrstu5": -300,
            "dummy": -300,
        },
        tip_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10,
            "U0123456789abcdefghijklmnopqrstu4": -10,
        },
        tip_prices={
            "U0123456789abcdefghijklmnopqrstu1": 100,
            "U0123456789abcdefghijklmnopqrstu4": -100,
        },
        sum_prices_with_tip={
            "U0123456789abcdefghijklmnopqrstu1": 1000,
            "U0123456789abcdefghijklmnopqrstu2": 1800,
            "U0123456789abcdefghijklmnopqrstu3": -1800,
            "U0123456789abcdefghijklmnopqrstu4": -400,
            "U0123456789abcdefghijklmnopqrstu5": -300,
            "dummy": -300,
        },
    ),
    Match(
        _id=3,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=0,
        created_at=datetime(2010, 1, 1, 1, 1, 3)
    ),
    Match(
        _id=4,
        line_group_id="dummy",
        status=2,
        created_at=datetime(2010, 1, 1, 1, 1, 4)
    ),
]

dummy_event = Event(
    type='message',
    source_type='group',
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type='text',
    text='_matches',
)


def test_execute():
    # Arrange
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyMatchesUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == 'このトークルームで行われた対戦一覧を表示します。第N回の詳細は「_match N」と送ってください。'
    assert reply_service.texts[1].text == '第1回 2010-01-01\n第2回 2010-01-01'


def test_execute_no_match():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyMatchesUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == 'まだ対戦結果がありません。'

