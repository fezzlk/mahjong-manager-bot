from application_models.page_contents import PageContents
from domain_model.entities.web_user import WebUser
from repositories import web_user_repository
from use_cases.web.approve_link_line_user_use_case import ApproveLinkLineUserUseCase


def test_execute_approves_line_link():
    # 目的: test_execute_approves_line_link の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: updated.is_approved_line_user is True
    # reply_service: なし
    # DB操作: created = web_user_repository.create(WebUser(user_code="c", name="n")); updated = web_user_repository.find_by_id(created._id)
    # Arrange
    created = web_user_repository.create(WebUser(user_code="c", name="n"))
    page_contents = PageContents(session={}, request=None)
    page_contents.login_user = created
    use_case = ApproveLinkLineUserUseCase()

    # Act
    use_case.execute(page_contents)

    # Assert
    updated = web_user_repository.find_by_id(created._id)
    assert updated.is_approved_line_user is True


def test_execute_sets_message():
    # 目的: test_execute_sets_message の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: page_contents.message が "LINEアカウント連携を承認しました。" である
    # reply_service: なし
    # DB操作: created = web_user_repository.create(WebUser(user_code="c2", name="n2"))
    # Arrange
    created = web_user_repository.create(WebUser(user_code="c2", name="n2"))
    page_contents = PageContents(session={}, request=None)
    page_contents.login_user = created
    use_case = ApproveLinkLineUserUseCase()

    # Act
    use_case.execute(page_contents)

    # Assert
    assert page_contents.message == "LINEアカウント連携を承認しました。"
