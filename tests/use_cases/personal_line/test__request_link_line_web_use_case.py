from datetime import datetime

import pytest

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.user import User, UserMode
from domain_model.entities.web_user import WebUser
from line_models.event import Event
from repositories import web_user_repository
from use_cases.personal_line.request_link_line_web_use_case import (
    RequestLinkLineWebUseCase,
)

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


@pytest.fixture(
    params=[
        (""),
        ("message"),
        ("message 1 2"),
    ],
)
def text_case(request) -> int:
    return request.param


def test_fail_mismatch_massage_format(text_case):
    # 目的: test_fail_mismatch_massage_format の挙動を検証する。
    # 入力: text_case
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / (
    # reply_service: texts
    # DB操作: なし
    # Arrange
    dummy_event = Event(
        type="message",
        source_type="user",
        user_id="U0123456789abcdefghijklmnopqrstu1",
        message_type="text",
        text=text_case,
    )
    request_info_service.set_req_info(event=dummy_event)
    use_case = RequestLinkLineWebUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == 'Web アカウントと紐付けするには "アカウント連携 [メールアドレス]" と送ってください。'
    )


def test_fail_no_web_user(mocker):
    # 目的: test_fail_no_web_user の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 2 件 / (
    # reply_service: texts
    # DB操作: web_user_repository.create(
    # Arrange
    dummy_event = Event(
        type="message",
        source_type="user",
        user_id="U0123456789abcdefghijklmnopqrstu1",
        message_type="text",
        text="アカウント連携 dummy@example.com",
    )
    request_info_service.set_req_info(event=dummy_event)
    use_case = RequestLinkLineWebUseCase()
    web_user_repository.create(
        WebUser(
            user_code="code1",
            name="name1",
            email="email1",
            linked_line_user_id=None,
            is_approved_line_user=False,
            created_at=datetime(2022, 1, 1, 12, 0, 0),
            updated_at=datetime(2022, 1, 1, 12, 0, 0),
        ),
    )

    mocker.patch(
        "use_cases.personal_line.request_link_line_web_use_case.url_for",
        return_value="",
    )
    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 2
    assert (
        reply_service.texts[0].text
        == "アカウント連携リクエストを受け付けました。ブラウザでログインし、承認してください。"
    )


def test_fail_have_linked_user(mocker):
    # 目的: test_fail_have_linked_user の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 2 件 / (
    # reply_service: texts
    # DB操作: web_user_repository.create(
    # Arrange
    dummy_event = Event(
        type="message",
        source_type="user",
        user_id="U0123456789abcdefghijklmnopqrstu1",
        message_type="text",
        text="アカウント連携 email1",
    )
    request_info_service.set_req_info(event=dummy_event)
    use_case = RequestLinkLineWebUseCase()
    web_user_repository.create(
        WebUser(
            user_code="code1",
            name="name1",
            email="email1",
            linked_line_user_id=None,
            is_approved_line_user=True,
            created_at=datetime(2022, 1, 1, 12, 0, 0),
            updated_at=datetime(2022, 1, 1, 12, 0, 0),
        ),
    )

    mocker.patch(
        "use_cases.personal_line.request_link_line_web_use_case.url_for",
        return_value="",
    )
    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 2
    assert (
        reply_service.texts[0].text
        == "アカウント連携リクエストを受け付けました。ブラウザでログインし、承認してください。"
    )


def test_fail_update_web_user(mocker):
    # 目的: test_fail_update_web_user の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "アカウント連携リクエストに失敗しました。" である
    # reply_service: texts
    # DB操作: web_user_repository.create(
    # Arrange
    dummy_event = Event(
        type="message",
        source_type="user",
        user_id="U0123456789abcdefghijklmnopqrstu1",
        message_type="text",
        text="アカウント連携 email1",
    )
    request_info_service.set_req_info(event=dummy_event)
    use_case = RequestLinkLineWebUseCase()
    web_user_repository.create(
        WebUser(
            user_code="code1",
            name="name1",
            email="email1",
            linked_line_user_id=None,
            is_approved_line_user=False,
            created_at=datetime(2022, 1, 1, 12, 0, 0),
            updated_at=datetime(2022, 1, 1, 12, 0, 0),
        ),
    )
    mocker.patch.object(
        web_user_repository,
        "update",
        return_value=0,
    )
    mocker.patch(
        "use_cases.personal_line.request_link_line_web_use_case.url_for",
        return_value="",
    )

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "アカウント連携リクエストに失敗しました。"


def test_success(mocker):
    # 目的: test_success の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 2 件 / (
    # reply_service: texts
    # DB操作: web_user_repository.create(
    # Arrange
    dummy_event = Event(
        type="message",
        source_type="user",
        user_id="U0123456789abcdefghijklmnopqrstu1",
        message_type="text",
        text="アカウント連携 email1",
    )
    request_info_service.set_req_info(event=dummy_event)
    use_case = RequestLinkLineWebUseCase()
    web_user_repository.create(
        WebUser(
            user_code="code1",
            name="name1",
            email="email1",
            linked_line_user_id=None,
            is_approved_line_user=False,
            created_at=datetime(2022, 1, 1, 12, 0, 0),
            updated_at=datetime(2022, 1, 1, 12, 0, 0),
        ),
    )

    mocker.patch(
        "use_cases.personal_line.request_link_line_web_use_case.url_for",
        return_value="",
    )
    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 2
    assert (
        reply_service.texts[0].text
        == "アカウント連携リクエストを送信しました。ブラウザでログインし、承認してください。"
    )
