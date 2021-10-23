from services import (
    request_info_service,
    reply_service,
    room_service,
)


class JoinRoomUseCase:

    def execute(self) -> None:
        reply_service.add_message(
            'こんにちは、今日は麻雀日和ですね。'
        )
        line_room_id = request_info_service.req_line_room_id
        if line_room_id is None:
            print('This request is not from room chat')
            return
        room_service.find_or_create(line_room_id)
