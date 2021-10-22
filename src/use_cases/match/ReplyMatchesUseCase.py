from services import (
    request_info_service,
    reply_service,
    match_service,
    hanchan_service,
    user_service,
    config_service,
)


class ReplyMatchesUseCase:

    def execute(self) -> None:
        line_room_id = request_info_service.req_line_room_id
        matches = match_service.get_archived(line_room_id)
        if matches is None:
            reply_service.add_message(
                'まだ対戦結果がありません。'
            )
            return

        reply_service.add_message(
            '最近の4試合の結果を表示します。詳細は「_match <ID>」')
        for match in matches[:4]:

            ids = match.hanchan_ids
            match_id = match._id
            is_required_sum = False
            date = match.created_at.strftime('%Y-%m-%d') + '\n'
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
