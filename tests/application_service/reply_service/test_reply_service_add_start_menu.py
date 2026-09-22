from application_service.reply_service import ReplyService


def test_success():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_start_menu()

    # Assert
    assert len(reply_service.buttons) == 1
    assert reply_service.buttons[0].quick_reply is None


def test_with_open_match_adds_new_match_quick_reply():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_start_menu(has_open_match=True)

    # Assert
    quick_reply = reply_service.buttons[0].quick_reply
    assert quick_reply is not None
    assert len(quick_reply.items) == 1
    assert quick_reply.items[0].action.data == "_new_match"


def test_without_open_match_has_no_quick_reply():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_start_menu(has_open_match=False)

    # Assert
    assert reply_service.buttons[0].quick_reply is None
