from application_service import (
    reply_service,
)
from use_cases.personal_line.reply_url_use_case import ReplyUrlUseCase


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件
    # reply_service: texts
    # DB操作: なし
    # Arrange
    use_case = ReplyUrlUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
