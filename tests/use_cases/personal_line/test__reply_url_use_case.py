from application_service import (
    reply_service,
)
from use_cases.personal_line.reply_url_use_case import ReplyUrlUseCase


def test_execute():
    # Arrange
    use_case = ReplyUrlUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
