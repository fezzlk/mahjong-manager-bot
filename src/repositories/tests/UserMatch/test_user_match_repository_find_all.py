from DomainModel.entities.User import User, UserMode
from DomainModel.entities.Match import Match
from DomainModel.entities.UserMatch import UserMatch
from repositories import (
    session_scope,
    user_repository,
    match_repository,
    user_match_repository,
)


dummy_users = [
    User(
        line_user_name="test_user1",
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        zoom_url="https://us00web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user1",
        matches=[],
        _id=1,
    ),
    User(
        line_user_name="test_user2",
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        zoom_url="https://us00web.zoom.us/j/01234567892?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user2",
        matches=[],
        _id=2,
    ),
]
dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[],
        users=[],
        status=1,
        _id=1,
    ),
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[],
        users=[],
        status=1,
        _id=2,
    ),
]


dummy_user_matches = [
    UserMatch(
        user_id=1,
        match_id=1,
    ),
    UserMatch(
        user_id=2,
        match_id=1,
    ),
    UserMatch(
        user_id=1,
        match_id=2,
    ),
]


def test_success():
    # Arrange
    with session_scope() as session:
        for dummy_user in dummy_users:
            user_repository.create(
                session,
                dummy_user,
            )
        for dummy_match in dummy_matches:
            match_repository.create(
                session,
                dummy_match,
            )
        for dummy_user_match in dummy_user_matches:
            user_match_repository.create(
                session,
                dummy_user_match,
            )

    # Act
    with session_scope() as session:
        result = user_match_repository.find_all(
            session,
        )

    # Assert
    expected_user_matches = [
        UserMatch(
            user_id=1,
            match_id=1,
        ),
        UserMatch(
            user_id=1,
            match_id=2,
        ),
        UserMatch(
            user_id=2,
            match_id=1,
        ),

    ]
    assert len(result) == len(dummy_user_matches)
    for i in range(len(result)):
        assert result[i].user_id == expected_user_matches[i].user_id
        assert result[i].match_id == expected_user_matches[i].match_id
