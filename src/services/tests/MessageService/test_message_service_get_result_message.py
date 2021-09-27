from services.MessageService import MessageService, result_messages
from tests.dummies import generate_dummy_user


def test_success():
    # Arrange
    message_service = MessageService()
    dummy_user = generate_dummy_user()

    # Act
    result = message_service.get_result_message(dummy_user.line_user_id)

    # Assert
    assert result in result_messages
