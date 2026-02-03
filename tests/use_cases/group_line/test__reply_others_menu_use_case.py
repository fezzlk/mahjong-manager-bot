from linebot.models import TemplateSendMessage

from application_service import (
    reply_service,
)
from use_cases.group_line.reply_others_menu_use_case import ReplyOthersMenuUseCase


def test_execute():
    # Arrange
    use_case = ReplyOthersMenuUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateSendMessage)
