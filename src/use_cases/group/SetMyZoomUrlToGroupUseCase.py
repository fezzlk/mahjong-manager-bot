from services import (
    request_info_service,
    user_service,
    reply_service,
    group_service,
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
            return

        reply_service.add_message(
            'Zoom URL を登録しました。\n「_zoom」で呼び出すことができます。')
