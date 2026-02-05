from domain_model.entities.user import User
from repositories import user_repository
from use_cases.web.get_users_for_web_use_case import GetUsersForWebUseCase


def test_execute_returns_users():
    # 目的: test_execute_returns_users の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: users の件数が 2 件
    # reply_service: なし
    # DB操作: user_repository.create(User(line_user_id="U1", line_user_name="A")); user_repository.create(User(line_user_id="U2", line_user_name="B"))
    # Arrange
    user_repository.create(User(line_user_id="U1", line_user_name="A"))
    user_repository.create(User(line_user_id="U2", line_user_name="B"))
    use_case = GetUsersForWebUseCase()

    # Act
    users = use_case.execute()

    # Assert
    assert len(users) == 2


def test_execute_returns_empty_list():
    # 目的: test_execute_returns_empty_list の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: users が [] である
    # reply_service: なし
    # DB操作: なし
    # Arrange
    use_case = GetUsersForWebUseCase()

    # Act
    users = use_case.execute()

    # Assert
    assert users == []
