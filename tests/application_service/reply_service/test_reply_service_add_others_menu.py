from linebot.v3.messaging import FlexButton, FlexMessage

from application_service.reply_service import ReplyService


def _button_actions(flex_message):
    return [
        c.action
        for bubble in flex_message.contents.contents
        for c in bubble.body.contents
        if isinstance(c, FlexButton)
    ]


def test_success():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_others_menu()

    # Assert: 対戦管理メニューはFlexCarouselで、FEZ-234の並び順どおり
    assert len(reply_service.buttons) == 1
    message = reply_service.buttons[0]
    assert isinstance(message, FlexMessage)
    assert [a.data for a in _button_actions(message)] == [
        "_active_match",
        "_new_match",
        "_sim",
        "_history_start",
        "_matches",
        "_ranking",
        "_rank",
        "_rank_detail",
    ]


def test_labels_within_line_limits():
    reply_service = ReplyService()
    reply_service.add_others_menu()
    message = reply_service.buttons[0]
    assert len(message.contents.contents) <= 12
    for action in _button_actions(message):
        assert len(action.label) <= 20
