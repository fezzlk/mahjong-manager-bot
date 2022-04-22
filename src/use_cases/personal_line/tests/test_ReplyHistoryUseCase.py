from use_cases.personal_line.ReplyHistoryUseCase import ReplyHistoryUseCase
from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainModel.entities.User import User, UserMode
from DomainModel.entities.Match import Match
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.UserMatch import UserMatch
from repositories import (
    session_scope,
    user_repository,
    match_repository,
    user_match_repository,
    hanchan_repository,
)
import pytest

dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    zoom_url="https://us00web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
    mode=UserMode.wait,
    jantama_name="jantama_user1",
    matches=[],
)

dummy_match = Match(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    hanchan_ids=[1],
    users=[],
    status=2,
)

dummy_user_match = UserMatch(
    user_id=1,
    match_id=1,
)

dummy_hanchan = Hanchan(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    raw_scores={
        "U0123456789abcdefghijklmnopqrstu1": 40000,
        "U0123456789abcdefghijklmnopqrstu2": 30000,
        "U0123456789abcdefghijklmnopqrstu3": 20000,
        "U0123456789abcdefghijklmnopqrstu4": 10000,
    },
    converted_scores={
        "U0123456789abcdefghijklmnopqrstu1": 50,
        "U0123456789abcdefghijklmnopqrstu2": 10,
        "U0123456789abcdefghijklmnopqrstu3": -20,
        "U0123456789abcdefghijklmnopqrstu4": -40,
    },
    match_id=1,
    status=1,
)


def test_execute_not_match():
    # Arrage
    with session_scope() as session:
        user_repository.create(session, dummy_user)

    request_info_service.req_line_user_id = dummy_user.line_user_id
    use_case = ReplyHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '対局履歴がありません。'


def test_execute():
    with pytest.raises(ValueError):
        # Arrage
        with session_scope() as session:
            user_repository.create(session, dummy_user)
            match_repository.create(session, dummy_match)
            user_match_repository.create(session, dummy_user_match)
            hanchan_repository.create(session, dummy_hanchan)

        request_info_service.req_line_user_id = dummy_user.line_user_id
        use_case = ReplyHistoryUseCase()

        # Act
        use_case.execute()

        # Assert
