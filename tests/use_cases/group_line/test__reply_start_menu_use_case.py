from linebot.models import TemplateSendMessage

from application_service import (
    reply_service,
)
from use_cases.group_line.reply_start_menu_use_case import ReplyStartMenuUseCase


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.buttons の件数が 1 件 / reply_service.buttons[0] が TemplateSendMessage 型
    # reply_service: buttons
    # DB操作: なし
    # Arrange
    use_case = ReplyStartMenuUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateSendMessage)
