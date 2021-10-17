from services import (
    request_info_service,
    reply_service,
    user_service,
    hanchan_service,
    match_service,
    config_service,
)


class MatchFinishUseCase:

    def execute(self):
        line_room_id = request_info_service.req_line_room_id
        if match_service.count_results(line_room_id) == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return

        current = match_service.get_current(line_room_id)

        ids = current.hanchan_ids
        match_id = current._id

        hanchans = hanchan_service.find_by_ids(ids)

        sum_hanchans = {}
        for i in range(len(ids)):
            converted_scores = hanchans[i].converted_scores

            for line_user_id, converted_score in converted_scores.items():
                if line_user_id not in sum_hanchans.keys():
                    sum_hanchans[line_user_id] = 0
                sum_hanchans[line_user_id] += converted_score

        reply_service.add_message(
            '\n'.join([
                f'{user_service.get_name_by_line_user_id(line_user_id)}: \
                    {converted_score}'
                for line_user_id, converted_score in sum_hanchans.items()
            ])
        )

        key = 'レート'
        reply_service.add_message(
            '対戦ID: ' + str(match_id) + '\n'.join([
                f'{user_service.get_name_by_line_user_id(line_user_id)}: \
                {converted_score * int(config_service.get_value_by_key(line_room_id, key)[1]) * 10}円 \
                ({"+" if converted_score > 0 else ""}{converted_score})'
                for line_user_id, converted_score in sum_hanchans.items()
            ])
        )

        match_service.archive(line_room_id)
