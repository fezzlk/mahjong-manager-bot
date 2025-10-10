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
        return_value=dummy_users,
    )

    # Act
    result = user_service.find_or_create_by_profile(profile=dummy_profile)

    # Assert
    assert isinstance(result, User)
    assert result.line_user_name == "test_user1"


def test_ok_no_user(mocker):
    # Arrange
    mocker.patch.object(
        user_repository,
        "find",
        return_value=[],
    )
    mock_create = mocker.patch.object(
        user_repository,
        "create",
    )

    # Act
    result = user_service.find_or_create_by_profile(profile=dummy_profile)

    # Assert
    assert result.line_user_name == "profile"
    mock_create.assert_called_once()
