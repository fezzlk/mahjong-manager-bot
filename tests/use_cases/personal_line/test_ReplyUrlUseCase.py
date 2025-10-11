from ApplicationService import (
    reply_service,
)
from use_cases.personal_line.ReplyUrlUseCase import ReplyUrlUseCase


def test_execute():
    # Arrange
    use_case = ReplyUrlUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
