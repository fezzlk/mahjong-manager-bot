from domain_model.entities.user import User
from repositories import user_repository
from use_cases.web.delete_users_for_web_use_case import DeleteUsersForWebUseCase


def test_execute_deletes_users_by_ids():
    # 目的: test_execute_deletes_users_by_ids の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: remaining の件数が 1 件 / remaining[0].line_user_id が "U2" である
    # reply_service: なし
    # DB操作: u1 = user_repository.create(User(line_user_id="U1", line_user_name="A")); u2 = user_repository.create(User(line_user_id="U2", line_user_name="B")); remaining = user_repository.find()
    # Arrange
    u1 = user_repository.create(User(line_user_id="U1", line_user_name="A"))
    user_repository.create(User(line_user_id="U2", line_user_name="B"))
    use_case = DeleteUsersForWebUseCase()

    # Act
    use_case.execute([u1._id])

    # Assert
    remaining = user_repository.find()
    assert len(remaining) == 1
    assert remaining[0].line_user_id == "U2"


def test_execute_with_empty_ids_does_nothing():
    # 目的: test_execute_with_empty_ids_does_nothing の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: remaining の件数が 1 件
    # reply_service: なし
    # DB操作: user_repository.create(User(line_user_id="U1", line_user_name="A")); remaining = user_repository.find()
    # Arrange
    user_repository.create(User(line_user_id="U1", line_user_name="A"))
    use_case = DeleteUsersForWebUseCase()

    # Act
    use_case.execute([])

    # Assert
    remaining = user_repository.find()
    assert len(remaining) == 1
