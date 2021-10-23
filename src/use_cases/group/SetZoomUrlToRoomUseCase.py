from services import (
    request_info_service,
    reply_service,
    user_service,
    room_service,
)


class SetZoomUrlToRoomUseCase:

    def execute(self, zoom_url: str) -> None:
        if zoom_url is None:
            line_user_id = request_info_service.req_line_user_id
            user = user_service.find_by_line_user_id(line_user_id)

            if user is None:
                print(
                    f'set_zoom_url: user(id={line_user_id}) is not found')
                return

            zoom_url = user.zoom_id

        line_room_id = request_info_service.req_line_room_id
        result_zoom_url = room_service.set_zoom_url(line_room_id, zoom_url)

        if result_zoom_url is None:
            return

        reply_service.add_message(
            'Zoom URL を登録しました。\n「_zoom」で呼び出すことができます。')
