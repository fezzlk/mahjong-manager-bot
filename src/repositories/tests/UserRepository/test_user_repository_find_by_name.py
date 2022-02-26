from typing import Tuple
import pytest
from repositories import session_scope, user_repository
from DomainModel.entities.User import User, UserMode


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
    User(
        line_user_name="test_user2",  # same name with id=2
        line_user_id="U0123456789abcdefghijklmnopqrstu3",
        zoom_url="https://us00web.zoom.us/j/01234567893?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user3",
        matches=[],
        _id=3,
    ),
]


@pytest.fixture(params=[
    (0),
    (1),  # hit multi users
])
def case(request) -> Tuple[int]:
    return request.param


def test_hit_1_record(case):
    # Arrange
    with session_scope() as session:
        for dummy_user in dummy_users:
            user_repository.create(
                session,
                dummy_user,
            )
    target_user = dummy_users[case]

    # Act
    with session_scope() as session:
        result = user_repository.find_by_name(
            session,
            target_user.line_user_name,
        )

    # Assert
        assert len(result) == 2
        for i in range(len(result)):
            assert isinstance(result[i], User)
            assert result[i]._id == target_user._id
            assert result[i].line_user_name == target_user.line_user_name
            assert result[i].line_user_id == target_user.line_user_id
            assert result[i].zoom_url == target_user.zoom_url
            assert result[i].mode == target_user.mode
            assert result[i].jantama_name == target_user.jantama_name
