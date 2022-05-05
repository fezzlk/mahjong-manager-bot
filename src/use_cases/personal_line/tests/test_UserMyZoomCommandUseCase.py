from use_cases.personal_line.UserMyZoomCommandUseCase import (
    UserMyZoomCommandUseCase,
)
from ApplicationService import (
    reply_service,
)


def test_execute():
    # Arrage
    use_case = UserMyZoomCommandUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[
        0].text == '_my_zoom コマンドはトークルームにて使用できます。\nユーザーに登録された URL をトークルームに紐づけることができます。\n(このチャットに Zoom URL を送ることでユーザーに URL を登録できます。）'
