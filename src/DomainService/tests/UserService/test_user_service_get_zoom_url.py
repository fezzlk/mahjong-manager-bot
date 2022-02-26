from werkzeug.exceptions import NotFound
import pytest
from DomainService.UserService import UserService
from repositories import session_scope, user_repository
from tests.dummies import generate_dummy_user_list

dummy_users = generate_dummy_user_list()[0:3]


def test_success():
    # Arrange
    user_service = UserService()
    dummy_user = dummy_users[0]
    with session_scope() as session:
        user_repository.create(session, dummy_user)

    # Act
    result = user_service.get_zoom_url(
        line_user_id=dummy_user.line_user_id,
    )

    # Assert
    assert result == dummy_user.zoom_url


def test_fail_with_invalid_mode():
    with pytest.raises(NotFound):
        # Arrange
        user_service = UserService()
        target_user = dummy_users[0]
        with session_scope() as session:
            user_repository.create(session, dummy_users[1])

        # Act
        user_service.get_zoom_url(
            line_user_id=target_user.line_user_id,
        )

        # Assert
