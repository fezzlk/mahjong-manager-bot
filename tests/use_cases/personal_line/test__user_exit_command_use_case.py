from application_service import (
    reply_service,
)
from domain_model.entities.user import User, UserMode
from repositories import (
    user_repository,
)
from use_cases.personal_line.user_exit_command_use_case import (
    UserExitCommandUseCase,
)

dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    mode=UserMode.wait.value,
    jantama_name="jantama_user1",
)


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: user.mode が UserMode.wait.value である / reply_service.texts の件数が 1 件
    # reply_service: texts
    # DB操作: user_repository.create(dummy_user); user = user_repository.find()[0]
    # Arrange
    user_repository.create(dummy_user)

    use_case = UserExitCommandUseCase()

    # Act
    use_case.execute(line_user_id=dummy_user.line_user_id)

    # Assert
    user = user_repository.find()[0]
    assert user.mode == UserMode.wait.value

    assert len(reply_service.texts) == 1
