from services.RichMenuService import RichMenuService
from tests.dummies import (
    generate_dummy_user,
)
from server import line_bot_api


def test_success(mocker):
    # Arrange
    rich_menu_service = RichMenuService()
    dummy_user = generate_dummy_user()

    mocker.patch.object(
        line_bot_api,
        'link_rich_menu_to_user',
        return_value=None
    )

    # Act
    rich_menu_service.create_and_link(dummy_user.line_user_id)

    # Assert
    # Do nothing
