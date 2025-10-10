from ApplicationService.RichMenuService import RichMenuService
from messaging_api_setting import line_bot_api
from dummies import (
    generate_dummy_user_list,
)


def test_success(mocker):
    # Arrange
    rich_menu_service = RichMenuService()
    dummy_user = generate_dummy_user_list()[0]

    mocker.patch.object(
        line_bot_api,
        "link_rich_menu_to_user",
        return_value=None,
    )
    mocker.patch.object(
        line_bot_api,
        "set_rich_menu_image",
        return_value=None,
    )

    # Act
    rich_menu_service.create_and_link(dummy_user.line_user_id)

    # Assert
    # Do nothing
