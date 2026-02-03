from linebot.models import TemplateSendMessage

from application_service import (
    reply_service,
)
from use_cases.group_line.reply_finish_confirm_use_case import ReplyFinishConfirmUseCase


def test_execute():
    # Arrange
    use_case = ReplyFinishConfirmUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateSendMessage)
