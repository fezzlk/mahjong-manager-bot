from tests.dummies import (
    generate_dummy_user_list,
    generate_dummy_profile,
)
from Services import UserService
from messaging_api_setting import line_bot_api
from Repositories import (
    user_repository, session_scope
)


def test_get_from_profile(mocker):
    # Arrage
    user_service = UserService()
    dummy_user = generate_dummy_user_list()[0]
    dummy_profile = generate_dummy_profile()
    mocker.patch.object(
        line_bot_api,
        'get_profile',
        return_value=dummy_profile,
    )

    # Act
    result = user_service.get_name_by_line_user_id(
        line_user_id=dummy_user.line_user_id,
    )

    # Assert
    assert result == dummy_profile.display_name


def test_get_from_db(mocker):
    # Arrage
    user_service = UserService()
    dummy_users = generate_dummy_user_list()[:3]
    with session_scope() as session:
        for dummy_user in dummy_users:
            user_repository.create(
                session=session,
                new_user=dummy_user,
            )

    mocker.patch.object(
        line_bot_api,
        'get_profile',
        side_effect=Exception,
    )

    # Act
    result = user_service.get_name_by_line_user_id(
        line_user_id=dummy_users[0].line_user_id,
    )

    # Assert
    assert result == dummy_users[0].line_user_name


def test_get_id_instead_of_name(mocker):
    # Arrage
    user_service = UserService()
    dummy_users = generate_dummy_user_list()[:3]
    with session_scope() as session:
        for dummy_user in dummy_users[1:3]:
            user_repository.create(
                session=session,
                new_user=dummy_user,
            )

    mocker.patch.object(
        line_bot_api,
        'get_profile',
        side_effect=Exception,
    )

    # Act
    result = user_service.get_name_by_line_user_id(
        line_user_id=dummy_users[0].line_user_id,
    )

    # Assert
    assert result == dummy_users[0].line_user_id
