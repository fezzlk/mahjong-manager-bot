from dummies import (
    generate_dummy_profile,
    generate_dummy_text_message_event_from_user,
)

from application_service import (
    reply_service,
    request_info_service,
    rich_menu_service,
)
from messaging_api_setting import line_bot_api
from use_cases.personal_line.follow_use_case import FollowUseCase


def test_execute(mocker):
    # 目的: test_execute の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件
    # reply_service: texts
    # DB操作: なし
    # Arrange
    dummy_event = generate_dummy_text_message_event_from_user()
    request_info_service.set_req_info(event=dummy_event)
    use_case = FollowUseCase()
    mocker.patch.object(
        rich_menu_service,
        "create_and_link",
        return_value=None,
    )
    mocker.patch.object(
        line_bot_api,
        "get_profile",
        return_value=generate_dummy_profile(),
    )

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
