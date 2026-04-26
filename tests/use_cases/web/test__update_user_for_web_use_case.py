from _web_test_utils import create_app, request_context

from domain_model.entities.user import User
from repositories import user_repository
from use_cases.web.update_user_for_web_use_case import UpdateUserForWebUseCase


def test_execute_updates_user_fields():
    # 目的: test_execute_updates_user_fields の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: updated.line_user_name が "A2" である / updated.jantama_name が "J" である
    # reply_service: なし
    # DB操作: created = user_repository.create(User(line_user_id="U1", line_user_name="A")); updated = user_repository.find({"_id": created._id})[0]
    # Arrange
    created = user_repository.create(User(line_user_id="U1", line_user_name="A"))
    app = create_app()
    use_case = UpdateUserForWebUseCase()

    form = {
        "_id": str(created._id),
        "line_user_name": "A2",
        "line_user_id": "U1",
        "mode": "UserMode.wait",
        "jantama_name": "J",
    }

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    updated = user_repository.find({"_id": created._id})[0]
    assert updated.line_user_name == "A2"
    assert updated.jantama_name == "J"


def test_execute_with_partial_fields():
    # 目的: test_execute_with_partial_fields の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: updated.line_user_name が "B2" である
    # reply_service: なし
    # DB操作: created = user_repository.create(User(line_user_id="U2", line_user_name="B")); updated = user_repository.find({"_id": created._id})[0]
    # Arrange
    created = user_repository.create(User(line_user_id="U2", line_user_name="B"))
    app = create_app()
    use_case = UpdateUserForWebUseCase()

    form = {
        "_id": str(created._id),
        "line_user_name": "B2",
        "line_user_id": "U2",
        "mode": "UserMode.wait",
    }

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    updated = user_repository.find({"_id": created._id})[0]
    assert updated.line_user_name == "B2"
