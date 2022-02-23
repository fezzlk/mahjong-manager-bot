from services.UserService import UserService
from repositories import session_scope, user_repository
from tests.dummies import generate_dummy_profile, generate_dummy_user_list
from domains.entities.User import User


def test_create_new_user():
    # Arrange
    user_service = UserService()
    dummy_profile = generate_dummy_profile()

    # Act
    result = user_service.find_or_create_by_profile(dummy_profile)

    # Assert
    assert isinstance(result, User)
    assert result.line_user_id == dummy_profile.user_id
    assert result.line_user_name == dummy_profile.display_name


def test_find_exist_user():
    # Arrange
    user_service = UserService()
    dummy_profile = generate_dummy_profile()
    dummy_user = generate_dummy_user_list()[4]
    with session_scope() as session:
        user_repository.create(session, dummy_user)

    # Act
    result = user_service.find_or_create_by_profile(dummy_profile)

    # Assert
    assert isinstance(result, User)
    assert result.line_user_id == dummy_user.line_user_id
    assert result.line_user_name == dummy_user.line_user_name
