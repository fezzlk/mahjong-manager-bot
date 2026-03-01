from _web_test_utils import create_app, request_context

from application_models.page_contents import PageContents, RegisterFormData
from use_cases.web.view_register_use_case import ViewRegisterUseCase


def test_execute_sets_form_defaults():
    # 目的: test_execute_sets_form_defaults の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result.page_title が "ユーザー登録" である / form.name.data が "Alice" である / form.email.data が "a@example.com" である
    # reply_service: なし
    # DB操作: なし
    # Arrange
    app = create_app()
    use_case = ViewRegisterUseCase()

    session_data = {"login_name": "Alice", "login_email": "a@example.com"}

    # Act
    with request_context(app, session_data=session_data):
        page_contents = PageContents(session=session_data, request=None, data_class=RegisterFormData)
        result, form = use_case.execute(page_contents)

    # Assert
    assert result.page_title == "ユーザー登録"
    assert form.name.data == "Alice"
    assert form.email.data == "a@example.com"


def test_execute_returns_form_instance():
    # 目的: test_execute_returns_form_instance の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result.page_title が "ユーザー登録" である / form is not None
    # reply_service: なし
    # DB操作: なし
    # Arrange
    app = create_app()
    use_case = ViewRegisterUseCase()
    session_data = {"login_name": "Bob", "login_email": "b@example.com"}

    # Act
    with request_context(app, session_data=session_data):
        page_contents = PageContents(session=session_data, request=None, data_class=RegisterFormData)
        result, form = use_case.execute(page_contents)

    # Assert
    assert result.page_title == "ユーザー登録"
    assert form is not None
