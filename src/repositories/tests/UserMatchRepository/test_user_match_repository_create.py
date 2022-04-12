from DomainModel.entities.User import User, UserMode
from DomainModel.entities.Match import Match
from DomainModel.entities.UserMatch import UserMatch
from repositories import (
    session_scope,
    user_repository,
    match_repository,
    user_match_repository,
)


dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    zoom_url="https://us00web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
    mode=UserMode.wait,
    jantama_name="jantama_user1",
    matches=[],
    _id=1,
)
dummy_match = Match(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    hanchan_ids=[1, 2, 3, 6, 7],
    users=[],
    status=1,
    _id=1,
)

dummy_user_match = UserMatch(
    user_id=1,
    match_id=1,
)


def test_success():
    # Arrange
    with session_scope() as session:
        user_repository.create(
            session,
            dummy_user,
        )
        match_repository.create(
            session,
            dummy_match,
        )

    # Act
    with session_scope() as session:
        result = user_match_repository.create(
            session,
            dummy_user_match,
        )

    # Assert
    assert isinstance(result, UserMatch)
    assert result.user_id == dummy_user_match.user_id
    assert result.match_id == dummy_user_match.match_id

    with session_scope() as session:
        record_on_db = user_match_repository.find_all(
            session,
        )
        assert len(record_on_db) == 1
        assert record_on_db[0].user_id == dummy_user_match.user_id
        assert record_on_db[0].match_id == dummy_user_match.match_id
