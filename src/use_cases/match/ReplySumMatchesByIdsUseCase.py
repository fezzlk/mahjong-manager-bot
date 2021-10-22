from typing import List
from services import (
    reply_service,
    match_service,
    hanchan_service,
    user_service,
    config_service,
    request_info_service,
)


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
        hanchan_ids = []
        for match in matches:
            hanchan_ids += match.hanchan_ids
            ids = hanchan_ids
            match_id = ','.join(formatted_id_list)
            is_required_sum = True
            date = ''
            hanchans = hanchan_service.find_by_ids(ids)

            sum_hanchans = {}
            for i in range(len(ids)):
                converted_scores = hanchans[i].converted_scores

                for user_id, converted_score in converted_scores.items():
                    if user_id not in sum_hanchans.keys():
                        sum_hanchans[user_id] = 0
                    sum_hanchans[user_id] += converted_score

            if is_required_sum:
                reply_service.add_message(
                    '\n'.join([
                        f'{user_service.get_name_by_line_user_id(user_id)}: {converted_score}'
                        for user_id, converted_score in sum_hanchans.items()
                    ])
                )

            key = 'レート'
            match_list = []
            line_room_id = request_info_service.req_line_room_id
            for line_user_id, converted_score in sum_hanchans.items():
                name = user_service.get_name_by_line_user_id(line_user_id)
                price = converted_score * int(config_service.get_value_by_key(line_room_id, key)[1]) * 10
                score = ("+" if converted_score > 0 else "") + converted_score
                match_list.append(f'{name}: {price}円 ({score})')

            reply_service.add_message(
                '対戦ID: ' + str(match_id) + '\n' + date + '\n'.join(match_list)
            )

