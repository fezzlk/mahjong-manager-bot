from linebot.models import (
    TextSendMessage,
)

import env_var
from ApplicationService.ReplyService import ReplyService
from messaging_api_setting import line_bot_api


def test_success(mocker):
    # Arrange
    reply_service = ReplyService()
    reply_service.texts = [TextSendMessage(text="dummy_text1"), TextSendMessage(text="dummy_text2")]

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
    mock_line_bot_api.assert_called_once_with(
        env_var.SERVER_ADMIN_LINE_USER_ID,
        [TextSendMessage(text="テストの画像アップロードに失敗しました\n送信者: dummy")])
