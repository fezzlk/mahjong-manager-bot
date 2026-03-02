from unittest.mock import MagicMock

from dummies import (
    generate_dummy_user_list,
)

from application_service.rich_menu_service import RichMenuService
from messaging_api_setting import line_bot_api


def test_success(mocker):
    # Arrange
    rich_menu_service = RichMenuService()
    dummy_user = generate_dummy_user_list()[0]

    mocker.patch.object(
        line_bot_api,
        "link_rich_menu_id_to_user",
        return_value=None,
    )
    mocker.patch.object(
        line_bot_api,
        "create_rich_menu",
        return_value=type("Response", (), {"rich_menu_id": "dummy_rich_menu_id"})(),
    )
    mock_blob_api = MagicMock()
    mocker.patch(
        "application_service.rich_menu_service.MessagingApiBlob",
        return_value=mock_blob_api,
    )

    # Act
    rich_menu_service.create_and_link(dummy_user.line_user_id)

    # Assert
    # Do nothing
