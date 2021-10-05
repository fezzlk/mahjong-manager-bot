# flake8: noqa: E999
from services import (
    request_info_service,
    reply_service,
    room_service,
    hanchan_service,
    matches_service,
)
from domains.Room import RoomMode


class StartInputUseCase:

    def execute(self):
        room_id = request_info_service.req_line_room_id
        current_match = matches_service.get_or_add_current(room_id)
        hanchan_service.add({}, room_id, current_match)

        room_service.chmod(
            room_id,
            RoomMode.input,
        )
        reply_service.add_message(
            f'第{matches_service.count_results(room_id)+1}回戦お疲れ様です。各自点数を入力してください。\
            \n（同点の場合は上家が高くなるように数点追加してください）')