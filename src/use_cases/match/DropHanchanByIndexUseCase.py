from services import (
    request_info_service,
    match_service,
    reply_service,
    hanchan_service,
)
import json


class DropHanchanByIndexUseCase:

    def execute(self, i: int) -> None:
        if match_service.count_results() == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。'
            )
            return
        current = match_service.get_current()
        result_ids = json.loads(current.result_ids)
        room_id = request_info_service.req_line_room_id
        hanchan_service.disabled_by_id(room_id, result_ids[i - 1])
        # reply_service.add_message(
        #     f'id={target_id}の結果を削除しました。'
        # )
        result_ids.pop(i - 1)
        match_service.update_hanchan_ids(result_ids)
