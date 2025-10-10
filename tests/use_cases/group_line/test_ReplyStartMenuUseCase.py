from linebot.models import TemplateSendMessage

from ApplicationService import (
    reply_service,
)
from use_cases.group_line.ReplyStartMenuUseCase import ReplyStartMenuUseCase


def test_execute():
    # Arrange
    use_case = ReplyStartMenuUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateSendMessage)
