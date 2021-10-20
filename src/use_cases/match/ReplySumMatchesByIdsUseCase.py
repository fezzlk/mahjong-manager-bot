from typing import List
from services import (
    reply_service,
    match_service,
    hanchan_service,
    user_service,
    config_service,
    request_info_service,
)
import json


class ReplySumMatchesByIdsUseCase:

    def execute(self, ids: List[str]) -> None:
        formatted_id_list = sorted(list(set(ids)))
        matches = match_service.get(ids)
        if len(matches) == 0:
            reply_service.add_message(
                '該当する対戦結果がありません。'
            )
            return
        reply_service.add_message(
            f'対戦ID={",".join(formatted_id_list)}の累計を表示します。'
        )
        result_ids = []
        for match in matches:
            result_ids += json.loads(match.result_ids)
            ids = result_ids
            match_id = ','.join(formatted_id_list)
            is_required_sum = True
            date = ''
            hanchans = hanchan_service.find_by_ids(ids)

            sum_hanchans = {}
            for i in range(len(ids)):
                converted_scores = json.loads(hanchans[i].converted_scores)

                for user_id, converted_score in converted_scores.items():
                    if user_id not in sum_hanchans.keys():
                        sum_hanchans[user_id] = 0
                    sum_hanchans[user_id] += converted_score

            if is_required_sum:
                reply_service.add_message(
                    '\n'.join([
                        f'{user_service.get_name_by_line_user_id(user_id)}: \
                            {converted_score}'
                        for user_id, converted_score in sum_hanchans.items()
                    ])
                )

            key = 'レート'
            room_id = request_info_service.req_line_room_id
            reply_service.add_message(
                '対戦ID: ' + str(match_id) + '\n' + date + '\n'.join([
                    f'{user_service.get_name_by_line_user_id(user_id)}: \
                    {converted_score * int(config_service.get_value_by_key(room_id, key)[1]) * 10}円 \
                    ({"+" if converted_score > 0 else ""}{converted_score})'
                    for user_id, converted_score in sum_hanchans.items()
                ])
            )
