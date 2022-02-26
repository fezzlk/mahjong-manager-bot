import pytest
from DomainService import UserService
from repositories import (
    user_repository, session_scope
)
from tests.dummies import generate_dummy_user_list
from werkzeug.exceptions import NotFound

dummy_users = generate_dummy_user_list()[0:3]


def test_success():
    # Arrage
    user_service = UserService()

    with session_scope() as session:
        for dummy_user in dummy_users:
            user_repository.create(
                session=session,
                new_user=dummy_user,
            )

    # Act
    result = user_service.get_mode(
        line_user_id=dummy_users[0].line_user_id,
    )

    # Assert
    assert result == dummy_users[0].mode


def test_fail_not_found():
    with pytest.raises(NotFound):
        # Arrage
        user_service = UserService()

        with session_scope() as session:
            for dummy_user in dummy_users[:2]:
                user_repository.create(
                    session=session,
                    new_user=dummy_user,
                )

        # Act
        user_service.get_mode(
            line_user_id=dummy_users[2].line_user_id,
        )

        # Assert
