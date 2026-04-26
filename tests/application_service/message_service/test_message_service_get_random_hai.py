from dummies import generate_dummy_user_list

from application_service.message_service import HAI, MessageService


def test_success():
    # Arrange
    message_service = MessageService()
    dummy_user = generate_dummy_user_list()[0]

    # Act
    result = message_service.get_random_hai(dummy_user.line_user_id)

    # Assert
    assert result in HAI
