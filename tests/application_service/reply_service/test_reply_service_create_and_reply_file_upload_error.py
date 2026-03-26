from linebot.v3.messaging import TextMessage

import env_var
from application_service.reply_service import ReplyService


def test_success(mocker):
    # Arrange
    reply_service = ReplyService()
    reply_service.texts = [TextMessage(text="dummy_text1"), TextMessage(text="dummy_text2")]

    mock_push = mocker.patch.object(reply_service, "push_a_message")

    # Act
    reply_service.create_and_reply_file_upload_error(
        title="テスト",
        sender="dummy",
    )

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "システムエラーが発生しました。"
    mock_push.assert_called_once_with(
        to=env_var.SERVER_ADMIN_LINE_USER_ID,
        message="テストの画像アップロードに失敗しました\n送信者: dummy",
    )
