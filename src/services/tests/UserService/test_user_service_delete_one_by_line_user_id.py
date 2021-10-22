from services.UserService import UserService
from repositories import session_scope, user_repository
from tests.dummies import generate_dummy_user_list


def test_success():
    # Arrange
    user_service = UserService()

    dummy_users = generate_dummy_user_list()[:3]
    dummy_user = dummy_users[0]
    with session_scope() as session:
        for user in dummy_users:
            user_repository.create(session, user)

    # Act
    user_service.delete_one_by_line_user_id(dummy_user.line_user_id)

    # Assert
    with session_scope() as session:
        result = user_repository.find_all(session)
        assert len(result) == 2


def test_not_hit():
    # Arrange
    user_service = UserService()

    dummy_users = generate_dummy_user_list()[:4]
    dummy_user = dummy_users[0]
    with session_scope() as session:
        for user in dummy_users[1:]:
            user_repository.create(session, user)

    # Act
    user_service.delete_one_by_line_user_id(dummy_user.line_user_id)

    # Assert
    with session_scope() as session:
        result = user_repository.find_all(session)
        assert len(result) == 3
