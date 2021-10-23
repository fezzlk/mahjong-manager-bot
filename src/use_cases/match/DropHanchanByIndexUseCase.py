from services import (
    request_info_service,
    match_service,
    reply_service,
    hanchan_service,
)


class DropHanchanByIndexUseCase:

    def execute(self, i: int) -> None:
        line_room_id = request_info_service.req_line_room_id
        if match_service.count_results(line_room_id) == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。'
            )
            return
        current = match_service.get_current(line_room_id)
        hanchan_ids = current.hanchan_ids
        room_id = request_info_service.req_line_room_id
        hanchan_service.disabled_by_id(room_id, hanchan_ids[i - 1])
        # reply_service.add_message(
        #     f'id={target_id}の結果を削除しました。'
        # )
        hanchan_ids.pop(i - 1)
        match_service.update_hanchan_ids(hanchan_ids)
