from use_cases import ReplyStartMenuUseCase
from Services import (
    reply_service,
)
from linebot.models import TemplateSendMessage


def test_execute():
    # Arrage
    use_case = ReplyStartMenuUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateSendMessage)
    reply_service.reset()
