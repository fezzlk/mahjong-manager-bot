from services import (
    request_info_service,
    room_service,
    reply_service,
)


class ReplyRoomModeUseCase:

    def execute(self):
        line_room_id = request_info_service.req_line_room_id
        mode = room_service.get_mode(line_room_id)
        reply_service.add_message(mode)
