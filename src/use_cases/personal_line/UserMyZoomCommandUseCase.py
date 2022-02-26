from ApplicationService import (
    reply_service,
)


class UserMyZoomCommandUseCase:

    def execute(self) -> None:
        reply_service.add_message(
            '_my_zoom コマンドはトークルームにて使用できます。\nユーザーに登録された URL をトークルームに紐づけることができます。\n(このチャットに Zoom URL を送ることでユーザーに URL を登録できます。）'
        )
