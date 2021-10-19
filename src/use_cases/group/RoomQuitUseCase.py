from domains.Room import RoomMode
from services import (
    request_info_service,
    reply_service,
    room_service,
    hanchan_service,
)


class RoomQuitUseCase:

    def execute(self, text):
        line_room_id = request_info_service.req_line_room_id
        hanchan_service.disable(line_room_id)
        room_service.chmod(
            line_room_id,
            RoomMode.wait,
        )
        reply_service.add_message(
            '始める時は「_start」と入力してください。')
