from services.MessageService import MessageService, wait_messages
from tests.dummies import generate_dummy_user


def test_success():
    # Arrange
    message_service = MessageService()
    dummy_user = generate_dummy_user()

    # Act
    result = message_service.get_wait_massage(dummy_user.line_user_id)

    # Assert
    assert result in wait_messages
