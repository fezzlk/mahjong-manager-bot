from typing import List, Tuple
import pytest
from repositories import session_scope, user_repository
from DomainModel.entities.User import User, UserMode


dummy_users = [
    User(
        line_user_name="test_user1",
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        mode=UserMode.wait.value,
        jantama_name="jantama_user1",
        matches=[],
        _id=1,
    ),
    User(
        line_user_name="test_user2",
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        mode=UserMode.wait.value,
        jantama_name="jantama_user2",
        matches=[],
        _id=2,
    ),
    User(
        line_user_name="test_user2",  # same name with _id=2
        line_user_id="U0123456789abcdefghijklmnopqrstu3",
        mode=UserMode.wait.value,
        jantama_name="jantama_user3",
        matches=[],
        _id=3,
    ),
]


@pytest.fixture(params=[
    # (dummy_users, length of result)
    (dummy_users[:1], 1),
    (dummy_users[1:3], 2),  # hit multi users
])
def case(request) -> Tuple[List[User], int]:
    return request.param


def test_success(case):
    # Arrange
    with session_scope() as session:
        for dummy_user in dummy_users:
            user_repository.create(
                session,
                dummy_user,
            )
    target_users = case[0]

    # Act
    with session_scope() as session:
        result = user_repository.find_by_name(
            session,
            target_users[0].line_user_name,
        )

    # Assert
        assert len(result) == case[1]
        for i in range(len(result)):
            assert isinstance(result[i], User)
            assert result[i]._id == target_users[i]._id
            assert result[i].line_user_name == target_users[i].line_user_name
            assert result[i].line_user_id == target_users[i].line_user_id
            assert result[i].mode == target_users[i].mode
            assert result[i].jantama_name == target_users[i].jantama_name
