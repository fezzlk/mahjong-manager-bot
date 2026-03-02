import pytest
from _web_test_utils import create_app, request_context

from application_models.page_contents import PageContents
from repositories import web_user_repository
from use_cases.web.register_web_user_use_case import RegisterWebUserUseCase


def test_execute_creates_web_user():
    # 目的: test_execute_creates_web_user の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: records の件数が 1 件 / records[0].name が "Alice" である
    # reply_service: なし
    # DB操作: records = web_user_repository.find({"user_code": "a@example.com"})
    # Arrange
    app = create_app()
    use_case = RegisterWebUserUseCase()

    form = {
        "name": "Alice",
        "email": "a@example.com",
    }

    # Act
    with request_context(app, form_data=form):
        from flask import request  # noqa: PLC0415
        page_contents = PageContents(session={}, request=request)
        page_contents.request = request
        use_case.execute(page_contents)

    # Assert
    records = web_user_repository.find({"user_code": "a@example.com"})
    assert len(records) == 1
    assert records[0].name == "Alice"


def test_execute_raises_for_invalid_form():
    # 目的: test_execute_raises_for_invalid_form の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: 明示的なassertなし（期待される挙動を説明）
    # reply_service: なし
    # DB操作: なし
    # Arrange
    app = create_app()
    use_case = RegisterWebUserUseCase()

    form = {
        "name": "",
        "email": "",
    }

    # Act / Assert
    with request_context(app, form_data=form):
        from flask import request  # noqa: PLC0415
        page_contents = PageContents(session={}, request=request)
        with pytest.raises(Exception):
            use_case.execute(page_contents)
