# flake8: noqa: E999
from server import line_bot_api, logger
from services import (
    request_info_service,
    reply_service,
    room_service,
)


class JoinRoomUseCase:

    def execute(self):
        """join room"""
        reply_service.add_message(
            'こんにちは、今日は麻雀日和ですね。'
        )
        room_id = request_info_service.req_line_room_id
        if room_id is None:
            logger.warning('This request is not from room chat')
            return
        room_service.find_or_create(room_id)
