from ApplicationService.ReplyService import ReplyService
from messaging_api_setting import line_bot_api


def test_reply_to_user(mocker):
    # Arrange
    reply_service = ReplyService()
    dummy_line_user_id = "U0123456789abcdefghijklmnopqrstu1"
    dummy_text = "hoge"

    mock = mocker.patch.object(
        line_bot_api,
        "push_message",
        return_value=None,
    )

    # Act
    reply_service.push_a_message(dummy_line_user_id, dummy_text)

    # Assert
    assert mock.call_count == 1
