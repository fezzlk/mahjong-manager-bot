# flake8: noqa: E999
from services import (
    request_info_service,
    reply_service,
    user_service,
    hanchan_service,
    matches_service,
    config_service,
)
import json


class MatchFinishUseCase:

    def execute(self, text):
        if matches_service.count_results() == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return
        current = matches_service.get_current()

        ids = json.loads(current.result_ids)
        match_id = current.id

        hanchans = hanchan_service.find_by_ids(ids)

        sum_hanchans = {}
        for i in range(len(ids)):
            converted_scores = json.loads(hanchans[i].converted_scores)

            for user_id, converted_score in converted_scores.items():
                if user_id not in sum_hanchans.keys():
                    sum_hanchans[user_id] = 0
                sum_hanchans[user_id] += converted_score

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
            '対戦ID: ' + str(match_id) + '\n'.join([
                f'{user_service.get_name_by_line_user_id(user_id)}: \
                {converted_score * int(config_service.get_by_key(room_id, key)[1]) * 10}円 \
                ({"+" if converted_score > 0 else ""}{converted_score})'
                for user_id, converted_score in sum_hanchans.items()
            ])
        )
        matches_service.archive()
