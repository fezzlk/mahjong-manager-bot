from DomainModel.entities.Match import Match
from DomainModel.entities.User import User
from use_cases.group_line.ReplyApplyBadaiUseCase import ReplyApplyBadaiUseCase
from ApplicationService import (
    request_info_service,
    reply_service,
)
from line_models.Event import Event
from repositories import (
    user_repository,
    match_repository,
)
from datetime import datetime

dummy_matches = [
    Match(
        _id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        created_at=datetime(2010, 1, 1, 1, 1, 1)
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

dummy_users = [
    User(
        _id=1,
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        line_user_name="test_user1",
    ),
    User(
        _id=2,
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        line_user_name="test_user2",
    ),
    User(
        _id=3,
        line_user_id="U0123456789abcdefghijklmnopqrstu3",
        line_user_name="test_user3",
    ),
    User(
        _id=4,
        line_user_id="U0123456789abcdefghijklmnopqrstu4",
        line_user_name="test_user4",
    ),
    User(
        _id=5,
        line_user_id="U0123456789abcdefghijklmnopqrstu5",
        line_user_name="test_user5",
    ),
]

dummy_event = Event(
    type='message',
    source_type='group',
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type='text',
    text='_badai 3,000',
)


def test_execute():
    # Arrange
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyApplyBadaiUseCase()

    # Act
    use_case.execute('3,000')

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == '直前の対戦の最終会計を表示します。'
    assert reply_service.texts[1].text == '対戦開始日: 2010年01月01日\n場代: 3000円(500円×6人)\ntest_user1: 500円\ntest_user2: 1300円\ntest_user3: -2300円\ntest_user4: -900円\ntest_user5: -800円\n友達未登録: -800円'


def test_execute_with_fraction():
    # Arrange
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyApplyBadaiUseCase()

    # Act
    use_case.execute('2,996')

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == '直前の対戦の最終会計を表示します。'
    assert reply_service.texts[1].text == '対戦開始日: 2010年01月01日\n場代: 2996円(500円×6人-4円)\ntest_user1: 500円\ntest_user2: 1300円\ntest_user3: -2300円\ntest_user4: -900円\ntest_user5: -800円\n友達未登録: -800円'


def test_execute_invalid_badai():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyApplyBadaiUseCase()

    # Act
    use_case.execute('dummy')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '場代は自然数で入力してください。'


def test_execute_no_match():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyApplyBadaiUseCase()

    # Act
    use_case.execute('0')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == 'まだ対戦結果がありません。'

def test_execute_with_progress_match():
    # Arrange
    progress_match = Match(
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
        },
    )
    match_repository.create(progress_match)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyApplyBadaiUseCase()

    # Act
    use_case.execute('2,996')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '現在進行中の対戦があります。対戦を終了するには「_finish」と送信してください。'


def test_execute_with_progress_match2():
    # Arrange
    progress_match = Match(
        _id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
    )
    match_repository.create(progress_match)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyApplyBadaiUseCase()

    # Act
    use_case.execute('2,996')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '現在進行中の対戦があります。対戦を終了するには「_finish」と送信してください。'
