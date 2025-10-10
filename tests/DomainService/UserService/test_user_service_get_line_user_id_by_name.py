from DomainModel.entities.User import User, UserMode
from DomainService import (
    user_service,
)
from line_models.Profile import Profile
from repositories import user_repository

dummy_users = [
    User(
        line_user_name="test_user1",
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        mode=UserMode.wait.value,
        jantama_name="jantama_user1",
    ),
    User(
        line_user_name="test_user1",
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        mode=UserMode.wait.value,
        jantama_name="jantama_user2",
    ),
]

dummy_profile = Profile(
    display_name="profile",
    user_id="U0123456789abcdefghijklmnopqrstu1",
)


def test_ok_hit_user(mocker):
    # Arrange
    mocker.patch.object(
        user_repository,
        "find",
        return_value=dummy_users[:1],
    )

    # Act
    result = user_service.get_line_user_id_by_name(line_user_name="test_user1")

    # Assert
    assert result == "U0123456789abcdefghijklmnopqrstu1"


def test_ok_no_user(mocker):
    # Arrange
    mocker.patch.object(
        user_repository,
        "find",
        return_value=[],
    )

    # Act
    result = user_service.get_line_user_id_by_name(line_user_name="test_user1")

    # Assert
    assert result is None


def test_ok_hit_multi_user(mocker):
    # Arrange
    mocker.patch.object(
        user_repository,
        "find",
        return_value=dummy_users,
    )

    # Act
    result = user_service.get_line_user_id_by_name(line_user_name="test_user1")

    # Assert
    assert result is None
