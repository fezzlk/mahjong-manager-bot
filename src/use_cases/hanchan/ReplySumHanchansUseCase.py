from services import (
    match_service,
    reply_service,
    hanchan_service,
    user_service,
    request_info_service,
)


class ReplySumHanchansUseCase:

    def execute(self) -> None:
        line_room_id = request_info_service.req_line_room_id
        if match_service.count_results(line_room_id) == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return
        match = match_service.get_current(line_room_id)

        ids = match.hanchan_ids
        date = match.created_at.strftime('%Y-%m-%d')
        hanchans = hanchan_service.find_by_ids(ids)

        hanchans_list = []
        sum_hanchans = {}

        for i in range(len(ids)):
            converted_scores = hanchans[i].converted_scores
            hanchans_list.append(
                f'第{i+1}回\n' + '\n'.join([
                    f'{user_service.get_name_by_line_user_id(r[0])}: {"+" if r[1] > 0 else ""}{r[1]}'
                    for r in sorted(
                        converted_scores.items(),
                        key=lambda x:x[1],
                        reverse=True
                    )
                ])
            )

            for user_id, converted_score in converted_scores.items():
                if user_id not in sum_hanchans.keys():
                    sum_hanchans[user_id] = 0

                sum_hanchans[user_id] += converted_score

        reply_service.add_message('\n\n'.join(hanchans_list))
        reply_service.add_message(
            '総計\n' + date + '\n' + '\n'.join([
                f'{user_service.get_name_by_line_user_id(r[0])}: {"+" if r[1] > 0 else ""}{r[1]}'
                for r in sorted(
                    sum_hanchans.items(),
                    key=lambda x:x[1],
                    reverse=True
                )
            ])
        )
