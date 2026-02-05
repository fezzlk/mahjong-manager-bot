from types import SimpleNamespace

from application_models.page_contents import PageContents, ViewUserInfoData
from domain_model.entities.web_user import WebUser
from repositories import web_user_repository
from use_cases.web.view_user_info_use_case import ViewUserInfoUseCase

from ._web_test_utils import create_app, request_context


def test_execute_sets_profile_without_line_link():
    # 目的: test_execute_sets_profile_without_line_link の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result.data.user_name が "Alice" である / result.data.user_email が "a@example.com" である / result.data.line_name が "未連携" である
    # reply_service: なし
    # DB操作: created = web_user_repository.create(WebUser(user_code="c", name="Alice", email="a@example.com"))
    # Arrange
    app = create_app()
    created = web_user_repository.create(WebUser(user_code="c", name="Alice", email="a@example.com"))
    use_case = ViewUserInfoUseCase()

    # Act
    with request_context(app, session_data={"login_user_id": created._id}):
        page_contents = PageContents(session={"login_user_id": created._id}, request=None, data_class=ViewUserInfoData)
        result = use_case.execute(page_contents)

    # Assert
    assert result.data.user_name == "Alice"
    assert result.data.user_email == "a@example.com"
    assert result.data.line_name == "未連携"


def test_execute_sets_profile_with_line_link(mocker):
    # 目的: test_execute_sets_profile_with_line_link の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result.data.line_name が "LineName" である
    # reply_service: なし
    # DB操作: created = web_user_repository.create(WebUser(user_code="c2", name="Bob", email="b@example.com", linked_line_user_id="U1", is_approved_line_user=True))
    # Arrange
    app = create_app()
    created = web_user_repository.create(WebUser(user_code="c2", name="Bob", email="b@example.com", linked_line_user_id="U1", is_approved_line_user=True))
    use_case = ViewUserInfoUseCase()

    # mock external API
    from messaging_api_setting import line_bot_api
    if line_bot_api is None:
        mocker.patch("messaging_api_setting.line_bot_api", SimpleNamespace(get_profile=lambda _: SimpleNamespace(display_name="LineName")))
    else:
        mocker.patch.object(line_bot_api, "get_profile", return_value=SimpleNamespace(display_name="LineName"))

    # Act
    with request_context(app, session_data={"login_user_id": created._id}):
        page_contents = PageContents(session={"login_user_id": created._id}, request=None, data_class=ViewUserInfoData)
        result = use_case.execute(page_contents)

    # Assert
    assert result.data.line_name == "LineName"
