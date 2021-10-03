from services import (
    request_info_service,
    reply_service,
    room_service,
    hanchans_service,
)


class RoomQuitUseCase:

    def execute(self, text):
        room_id = request_info_service.req_line_room_id
        hanchans_service.disable(room_id)
        room_service.chmod(
            room_id,
            room_service.modes.wait,
        )
        reply_service.add_message(
            '始める時は「_start」と入力してください。')
