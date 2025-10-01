from ApplicationService import (
    reply_service,
)
from DomainModel.entities.User import User, UserMode
from repositories import (
    user_repository,
)
from use_cases.personal_line.UserExitCommandUseCase import (
    UserExitCommandUseCase,
)

dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    mode=UserMode.wait.value,
    jantama_name="jantama_user1",
)


def test_execute():
    # Arrange
    user_repository.create(dummy_user)

    use_case = UserExitCommandUseCase()

    # Act
    use_case.execute(line_user_id=dummy_user.line_user_id)

    # Assert
    user = user_repository.find()[0]
    assert user.mode == UserMode.wait.value

    assert len(reply_service.texts) == 1
