import requests

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.user import User, UserMode
from line_models.event import Event
from repositories import user_repository
from use_cases.personal_line.reply_token_use_case import ReplyTokenUseCase

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


class Dummy:
    def json(self):
        return


def test_execute(mocker):
    # 目的: test_execute の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "JWT hoge" である
    # reply_service: texts
    # DB操作: user_repository.create(dummy_user)
    # Arrange
    user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyTokenUseCase()
    dummy_response = Dummy()
    mocker.patch.object(
        requests,
        "post",
        return_value=dummy_response,
    )
    mocker.patch.object(
        dummy_response,
        "json",
        return_value={"access_token": "hoge"},
    )

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "JWT hoge"


def test_execute_no_user(mocker):
    # 目的: test_execute_no_user の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "ユーザが登録されていません。友達追加し直してください。" である
    # reply_service: texts
    # DB操作: なし
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyTokenUseCase()
    dummy_response = Dummy()
    mocker.patch.object(
        requests,
        "post",
        return_value=dummy_response,
    )
    mocker.patch.object(
        dummy_response,
        "json",
        return_value={"access_token": "hoge"},
    )

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "ユーザが登録されていません。友達追加し直してください。"
