from DomainService import (
    user_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)


class SetZoomUrlToUserUseCase:

    def execute(self, zoom_url: str) -> None:
        line_user_id = request_info_service.req_line_user_id
        result = user_service.set_zoom_url(line_user_id, zoom_url)

        if result is None:
            reply_service.add_message(
                'Zoom URL の登録に失敗しました。')
            return

        reply_service.add_message(
            'Zoom URL を登録しました。\nトークルームにて「_my_zoom」で呼び出すことができます。')
