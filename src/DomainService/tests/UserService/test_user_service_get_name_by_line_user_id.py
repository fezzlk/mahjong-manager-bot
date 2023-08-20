from tests.dummies import generate_dummy_user_list
from DomainService import user_service
from repositories import user_repository
from messaging_api_setting import line_bot_api


def test_success_with_line_api(mocker):
    # Arrange
    dummy_users = generate_dummy_user_list()
    for dummy_user in dummy_users:
        user_repository.create(
            dummy_user,
        )
    mocker.patch.object(
        line_bot_api,
        'get_profile',
        return_value='username from line api',
    )

    # Act
    result = user_service.get_name_by_line_user_id(dummy_users[0].line_user_id)

    # Assert
    assert result == dummy_users[0].line_user_name


def test_success_from_db():
    # Arrange
    dummy_users = generate_dummy_user_list()
    for dummy_user in dummy_users:
        user_repository.create(
            dummy_user,
        )

    # Act
    result = user_service.get_name_by_line_user_id(dummy_users[0].line_user_id)

    # Assert
    assert result == dummy_users[0].line_user_name


def test_success_return_id():
    # Arrange

    # Act
    result = user_service.get_name_by_line_user_id('dummy_line_id')

    # Assert
    assert result is None
