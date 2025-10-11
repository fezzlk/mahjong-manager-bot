from ApplicationService.ReplyService import ReplyService


def test_success():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_confirm_finish_menu()

    # Assert
    assert len(reply_service.buttons) == 1
