from ApplicationService.ReplyService import ReplyService


def test_success():
    # Arrange
    reply_service = ReplyService()
    reply_service.texts = ["dummy_text"]
    reply_service.buttons = ["dummy_button"]
    reply_service.images = ["dummy_image"]

    # Act
    reply_service.reset()

    # Assert
    assert len(reply_service.texts) == 0
    assert len(reply_service.buttons) == 0
    assert len(reply_service.images) == 0
