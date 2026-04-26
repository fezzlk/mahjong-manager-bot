from domain_model.entities.user import User
from repositories import user_repository
from use_cases.web.get_user_for_web_use_case import GetUserForWebUseCase


def test_execute_returns_user_by_id():
    # 目的: test_execute_returns_user_by_id の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: user is not None / user.line_user_id が "U1" である
    # reply_service: なし
    # DB操作: created = user_repository.create(User(line_user_id="U1", line_user_name="A"))
    # Arrange
    created = user_repository.create(User(line_user_id="U1", line_user_name="A"))
    use_case = GetUserForWebUseCase()

    # Act
    user = use_case.execute(created._id)

    # Assert
    assert user is not None
    assert user.line_user_id == "U1"


def test_execute_returns_none_for_missing_id():
    # 目的: test_execute_returns_none_for_missing_id の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: user is None
    # reply_service: なし
    # DB操作: なし
    # Arrange
    use_case = GetUserForWebUseCase()

    # Act
    user = use_case.execute("000000000000000000000000")

    # Assert
    assert user is None
