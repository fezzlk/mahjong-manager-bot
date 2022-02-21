from services.MessageService import MessageService, finish_hanchan_messages


def test_success():
    # Arrange
    message_service = MessageService()

    # Act
    result = message_service.get_finish_hanchan_message()

    # Assert
    assert result in finish_hanchan_messages
