from tests.dummies import generate_dummy_user_list
from repositories import session_scope, user_repository
from domains.User import User


def test_hit_1_record():
    # Arrange
    dummy_users = generate_dummy_user_list()[:3]
    with session_scope() as session:
        for dummy_user in dummy_users:
            user_repository.create(
                session,
                dummy_user,
            )
    target_user = dummy_users[0]

    # Act
    with session_scope() as session:
        result = user_repository.find_one_by_line_user_id(
            session,
            target_user.line_user_id,
        )

    # Assert
        assert isinstance(result, User)
        assert result._id == target_user._id
        assert result.line_user_name == target_user.line_user_name
        assert result.line_user_id == target_user.line_user_id
        assert result.zoom_url == target_user.zoom_url
        assert result.mode == target_user.mode
        assert result.jantama_name == target_user.jantama_name


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_users = generate_dummy_user_list()[:2]
        for dummy_user in dummy_users:
            user_repository.create(
                session,
                dummy_user,
            )
    target_user = generate_dummy_user_list()[2]

    # Act
    with session_scope() as session:
        result = user_repository.find_one_by_line_user_id(
            session,
            target_user.line_user_id,
        )

    # Assert
        assert result is None
