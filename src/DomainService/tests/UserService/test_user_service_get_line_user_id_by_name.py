import pytest
from DomainModel.entities.User import User, UserMode
from DomainService import UserService
from repositories import (
    user_repository, session_scope
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


def test_success_get_line_user_id():
    # Arrage
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
        # Arrage
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
