from services import (
    request_info_service,
    reply_service,
    room_service,
)


class ReplyRoomZoomUrlUseCase:

    def execute(self):
        line_room_id = request_info_service.req_line_room_id
        result_zoom_url = room_service.get_zoom_url(line_room_id)

        if result_zoom_url is None:
            reply_service.add_message('Zoom URL を取得できませんでした。')
            return

        reply_service.add_message(result_zoom_url)
