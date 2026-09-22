from application_service.reply_service import ReplyService


def test_success():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_others_menu()

    # Assert
    assert len(reply_service.buttons) == 1
    quick_reply = reply_service.buttons[0].quick_reply
    assert quick_reply is not None
    data_values = [item.action.data for item in quick_reply.items]
    assert data_values == ["_sum_matches", "_help"]
