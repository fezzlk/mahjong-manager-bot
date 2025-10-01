from linebot.models import TemplateSendMessage

from ApplicationService import (
    reply_service,
)
from use_cases.group_line.ReplyOthersMenuUseCase import ReplyOthersMenuUseCase


def test_execute():
    # Arrange
    use_case = ReplyOthersMenuUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateSendMessage)
