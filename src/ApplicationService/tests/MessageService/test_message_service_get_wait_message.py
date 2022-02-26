from ApplicationService.MessageService import MessageService, wait_messages


def test_success():
    # Arrange
    message_service = MessageService()

    # Act
    result = message_service.get_wait_massage()

    # Assert
    assert result in wait_messages
