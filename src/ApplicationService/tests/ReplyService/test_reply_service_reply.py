from ApplicationService.ReplyService import ReplyService
from tests.dummies import (
    generate_dummy_follow_event,
    generate_dummy_text_message_event_from_group,
    generate_dummy_text_message_event_from_user,
)
from linebot.models import (
    TextSendMessage,
)
from messaging_api_setting import line_bot_api


def test_reply_to_user(mocker):
    # Arrange
    reply_service = ReplyService()
    dummy_event = generate_dummy_text_message_event_from_user()
    dummy_text = 'dummy_text'
    reply_service.texts = [
        TextSendMessage(text=dummy_text)
    ]

    mock = mocker.patch.object(
        line_bot_api,
        'reply_message',
        return_value=None,
    )

    # Act
    reply_service.reply(dummy_event)

    # Assert
    assert len(reply_service.texts) == 1
    mock.assert_called_once()


def test_reply_to_group(mocker):
    # Arrange
    reply_service = ReplyService()
    dummy_event = generate_dummy_follow_event()
    dummy_text = 'dummy_text'
    reply_service.texts = [
        TextSendMessage(text=dummy_text)
    ]

    mock = mocker.patch.object(
        line_bot_api,
        'reply_message',
        return_value=None,
    )

    # Act
    reply_service.reply(dummy_event)

    # Assert
    assert len(reply_service.texts) == 1
    mock.assert_called_once()


def test_content_0(mocker):
    # Arrange
    reply_service = ReplyService()
    dummy_event = generate_dummy_text_message_event_from_group()

    # Act
    reply_service.reply(dummy_event)

    # Assert
    assert len(reply_service.texts) == 0
