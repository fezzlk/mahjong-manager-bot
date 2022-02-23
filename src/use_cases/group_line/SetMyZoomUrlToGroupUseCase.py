from DomainService import (
    user_service,
    group_service,
)

from ApplicationService import (
    request_info_service,
    reply_service,
)


class SetMyZoomUrlToGroupUseCase:

    def execute(self) -> None:
        line_user_id = request_info_service.req_line_user_id
        zoom_url = user_service.get_zoom_url(line_user_id)
        if zoom_url is None:
            reply_service.add_message(
                'Zoom URL を取得できませんでした。')
            return
        reply_service.add_message(zoom_url)

        line_group_id = request_info_service.req_line_group_id
        result_zoom_url = group_service.set_zoom_url(line_group_id, zoom_url)

        if result_zoom_url is None:
            reply_service.add_message(
                'トークルームが登録されていません。招待し直してください。')
            return

        reply_service.add_message(
            'Zoom URL を登録しました。\n「_zoom」で呼び出すことができます。')
