from services import (
    request_info_service,
    reply_service,
    room_service,
    hanchan_service,
    match_service,
)
from domains.Room import RoomMode


class StartInputUseCase:

    def execute(self) -> None:
        line_room_id = request_info_service.req_line_room_id

        if room_service.get_mode(line_room_id) == RoomMode.input:
            reply_service.add_message('すでに入力モードです')
            return

        current_match = match_service.get_or_create_current(line_room_id)
        hanchan_service.create({}, line_room_id, current_match)

        room_service.chmod(
            line_room_id,
            RoomMode.input,
        )
        reply_service.add_message(
            f'第{match_service.count_results(line_room_id)+1}回戦お疲れ様です。各自点数を入力してください。\
            \n（同点の場合は上家が高くなるように数点追加してください）')
