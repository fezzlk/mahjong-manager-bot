from dummies import (
    generate_dummy_join_event,
)

from application_service import reply_service, request_info_service
from use_cases.common_line.reply_github_url_use_case import ReplyGitHubUrlUseCase


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "https://github.com/bbladr/mahjong-manager-bot" である
    # reply_service: texts
    # DB操作: なし
    # Arrange
    dummy_event = generate_dummy_join_event()
    request_info_service.set_req_info(event=dummy_event)

    use_case = ReplyGitHubUrlUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "https://github.com/bbladr/mahjong-manager-bot"
