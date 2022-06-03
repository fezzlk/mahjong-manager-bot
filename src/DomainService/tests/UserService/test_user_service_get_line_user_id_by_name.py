import pytest
from DomainService import UserService
from repositories import (
    user_repository, session_scope
)
from tests.dummies import generate_dummy_user_list

dummy_users = generate_dummy_user_list()[1:4]


def test_success_get_line_user_id():
    # Arrange
    user_service = UserService()

    with session_scope() as session:
        for dummy_user in dummy_users:
            user_repository.create(
                session=session,
                new_user=dummy_user,
            )

    # Act
    result = user_service.get_line_user_id_by_name(
        line_user_name=dummy_users[0].line_user_name,
    )

    # Assert
    assert result == dummy_users[0].line_user_id


def test_fail_because_hit_multi_user():
    with pytest.raises(ValueError):
        # Arrange
        user_service = UserService()

        with session_scope() as session:
            for dummy_user in dummy_users:
                user_repository.create(
                    session=session,
                    new_user=dummy_user,
                )

        # Act
        user_service.get_line_user_id_by_name(
            line_user_name=dummy_users[1].line_user_name,
        )

        # Assert
