from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.user import User, UserMode
from line_models.event import Event
from repositories import user_repository
from use_cases.personal_line.reply_user_mode_use_case import ReplyUserModeUseCase

dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    mode=UserMode.wait.value,
    jantama_name="jantama_user1",
)

dummy_event = Event(
    type="message",
    source_type="user",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="dummy_text",
)


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "wait" である
    # reply_service: texts
    # DB操作: user_repository.create(dummy_user)
    # Arrange
    user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyUserModeUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "wait"



def test_execute_no_user():
    # 目的: test_execute_no_user の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "ユーザーを認識できませんでした。当アカウントを一度ブロックし、ブロック解除してください。" である
    # reply_service: texts
    # DB操作: なし
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyUserModeUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "ユーザーを認識できませんでした。当アカウントを一度ブロックし、ブロック解除してください。"
