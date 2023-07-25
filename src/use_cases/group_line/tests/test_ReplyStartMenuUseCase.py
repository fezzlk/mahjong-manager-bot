from use_cases.group_line.ReplyStartMenuUseCase import ReplyStartMenuUseCase
from ApplicationService import (
    reply_service,
)
from linebot.models import TemplateSendMessage


def test_execute():
    # Arrange
    use_case = ReplyStartMenuUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateSendMessage)
