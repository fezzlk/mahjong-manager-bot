from dummies import (
    generate_dummy_text_message_event_from_group,
)

from application_service import (
    reply_service,
    request_info_service,
)
from use_cases.group_line.reply_group_help_use_case import ReplyGroupHelpUseCase


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 2 件
    # reply_service: texts
    # DB操作: なし
    # Arrange
    dummy_event = generate_dummy_text_message_event_from_group()
    request_info_service.set_req_info(event=dummy_event)

    use_case = ReplyGroupHelpUseCase()

    # Act
    use_case.execute([])

    # Assert
    assert len(reply_service.texts) == 2
