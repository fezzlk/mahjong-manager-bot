from services.ReplyService import ReplyService


def test_success():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_others_menu()

    # Assert
    assert len(reply_service.buttons) == 1
