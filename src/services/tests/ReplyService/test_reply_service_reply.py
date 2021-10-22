from services.ReplyService import ReplyService
from tests.dummies import (
    generate_dummy_follow_event,
    generate_dummy_text_message_event_from_room,
    generate_dummy_text_message_event_from_user,
)
from linebot.models import (
    TextSendMessage,
)
from server import line_bot_api


def test_reply_to_user(mocker):
    # Arrange
    reply_service = ReplyService()
    dummy_event = generate_dummy_text_message_event_from_user()
    dummy_text = 'dummy_text'
    reply_service.texts = [
        TextSendMessage(text=dummy_text)
    ]

    mocker.patch.object(
        line_bot_api,
        'reply_message',
        return_value=None,
    )

    # Act
    reply_service.reply(dummy_event)

    # Assert
    assert len(reply_service.texts) == 0


def test_reply_to_room(mocker):
    # Arrange
    reply_service = ReplyService()
    dummy_event = generate_dummy_follow_event()
    dummy_text = 'dummy_text'
    reply_service.texts = [
        TextSendMessage(text=dummy_text)
    ]

    mocker.patch.object(
        line_bot_api,
        'reply_message',
        return_value=None,
    )

    # Act
    reply_service.reply(dummy_event)

    # Assert
    assert len(reply_service.texts) == 0


def test_content_0(mocker):
    # Arrange
    reply_service = ReplyService()
    dummy_event = generate_dummy_text_message_event_from_room()

    # Act
    reply_service.reply(dummy_event)

    # Assert
    assert len(reply_service.texts) == 0


def test_not_reply(mocker):
    # Arrange
    reply_service = ReplyService()
    dummy_event = generate_dummy_text_message_event_from_room()
    dummy_text = 'dummy_text'
    reply_service.texts = [
        TextSendMessage(text=dummy_text)
    ]

    # Act
    reply_service.reply(dummy_event)

    # Assert
    assert len(reply_service.texts) == 0