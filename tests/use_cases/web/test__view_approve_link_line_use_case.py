from application_models.page_contents import PageContents
from domain_model.entities.user import User
from domain_model.entities.web_user import WebUser
from repositories import user_repository, web_user_repository
from use_cases.web.view_approve_link_line_use_case import ViewApproveLinkLineUseCase


def test_execute_sets_line_user_name():
    # 目的: test_execute_sets_line_user_name の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result.line_user_name が "Alice" である
    # reply_service: なし
    # DB操作: line_user = user_repository.create(User(line_user_id="U1", line_user_name="Alice")); web_user = web_user_repository.create(WebUser(user_code="c", linked_line_user_id="U1"))
    # Arrange
    user_repository.create(User(line_user_id="U1", line_user_name="Alice"))
    web_user = web_user_repository.create(WebUser(user_code="c", linked_line_user_id="U1"))
    page_contents = PageContents(session={}, request=None)
    page_contents.login_user = web_user
    use_case = ViewApproveLinkLineUseCase()

    # Act
    result = use_case.execute(page_contents)

    # Assert
    assert result.line_user_name == "Alice"


def test_execute_when_no_linked_user():
    # 目的: test_execute_when_no_linked_user の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result.line_user_name が "" である
    # reply_service: なし
    # DB操作: web_user = web_user_repository.create(WebUser(user_code="c2", linked_line_user_id=""))
    # Arrange
    web_user = web_user_repository.create(WebUser(user_code="c2", linked_line_user_id=""))
    page_contents = PageContents(session={}, request=None)
    page_contents.login_user = web_user
    use_case = ViewApproveLinkLineUseCase()

    # Act
    result = use_case.execute(page_contents)

    # Assert
    assert result.line_user_name == ""
