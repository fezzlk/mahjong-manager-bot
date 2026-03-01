from linebot.v3.messaging import TextMessage

import env_var
from application_service.reply_service import ReplyService
from messaging_api_setting import line_bot_api


def test_success(mocker):
    # Arrange
    reply_service = ReplyService()
    reply_service.texts = [TextMessage(text="dummy_text1"), TextMessage(text="dummy_text2")]

    mock_line_bot_api = mocker.patch.object(
        line_bot_api,
        "push_message",
    )

    # Act
    reply_service.create_and_reply_file_upload_error(
        title="テスト",
        sender="dummy",
    )

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "システムエラーが発生しました。"
    mock_line_bot_api.assert_called_once()
    call_arg = mock_line_bot_api.call_args[0][0]
    assert call_arg.to == env_var.SERVER_ADMIN_LINE_USER_ID
    assert len(call_arg.messages) == 1
    assert call_arg.messages[0].text == "テストの画像アップロードに失敗しました\n送信者: dummy"
