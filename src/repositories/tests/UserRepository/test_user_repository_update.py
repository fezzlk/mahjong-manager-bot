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
        _id=1,
    ),
]


def test_hit_1_record():
    # Arrange
    dummy_user = dummy_users[0]
    updated_user = dummy_users[1]
    with session_scope() as session:
        user_repository.create(
            session,
            dummy_user,
        )

    # Act
    with session_scope() as session:
        user_repository.update(
            session,
            updated_user,
        )

    # Assert
    with session_scope() as session:
        result = user_repository.find(session)[0]
        assert isinstance(result, User)
        assert result._id == updated_user._id
        assert result.line_user_name == updated_user.line_user_name
        assert result.line_user_id == updated_user.line_user_id
        assert result.mode == updated_user.mode
        assert result.jantama_name == updated_user.jantama_name


def test_hit_0_record():
    # Arrange

    # Act
    with session_scope() as session:
        result = user_repository.update(
            session,
            dummy_users[0],
        )

    # Assert
    assert result == 0
