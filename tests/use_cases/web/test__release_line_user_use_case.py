from application_models.page_contents import PageContents
from domain_model.entities.web_user import WebUser
from repositories import web_user_repository
from use_cases.web.release_line_user_use_case import ReleaseLineUserUseCase


def test_execute_resets_link_and_approval():
    # 目的: test_execute_resets_link_and_approval の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: updated.linked_line_user_id が "" である / updated.is_approved_line_user is False
    # reply_service: なし
    # DB操作: created = web_user_repository.create(WebUser(user_code="c", name="n", linked_line_user_id="U1", is_approved_line_user=True)); updated = web_user_repository.find_by_id(created._id)
    # Arrange
    created = web_user_repository.create(WebUser(user_code="c", name="n", linked_line_user_id="U1", is_approved_line_user=True))
    page_contents = PageContents(session={}, request=None)
    page_contents.login_user = created
    use_case = ReleaseLineUserUseCase()

    # Act
    use_case.execute(page_contents)

    # Assert
    updated = web_user_repository.find_by_id(created._id)
    assert updated.linked_line_user_id == ""
    assert updated.is_approved_line_user is False


def test_execute_sets_message():
    # 目的: test_execute_sets_message の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: page_contents.message が "LINEアカウント連携を解除しました。" である
    # reply_service: なし
    # DB操作: created = web_user_repository.create(WebUser(user_code="c2", name="n2", linked_line_user_id="U2", is_approved_line_user=True))
    # Arrange
    created = web_user_repository.create(WebUser(user_code="c2", name="n2", linked_line_user_id="U2", is_approved_line_user=True))
    page_contents = PageContents(session={}, request=None)
    page_contents.login_user = created
    use_case = ReleaseLineUserUseCase()

    # Act
    use_case.execute(page_contents)

    # Assert
    assert page_contents.message == "LINEアカウント連携を解除しました。"
