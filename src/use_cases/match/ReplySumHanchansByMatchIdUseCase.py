from Services import (
    match_service,
    reply_service,
    hanchan_service,
    user_service,
)


class ReplySumHanchansByMatchIdUseCase:

    def execute(self, match_id: int) -> None:
        match = match_service.get(match_id)

        ids = match.hanchan_ids
        date = match.created_at.strftime('%Y-%m-%d') + '\n',
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

            for line_user_id, converted_score in converted_scores.items():
                if line_user_id not in sum_hanchans.keys():
                    sum_hanchans[line_user_id] = 0

                sum_hanchans[line_user_id] += converted_score

        reply_service.add_message('\n\n'.join(hanchans_list))
        reply_service.add_message(
            '総計\n' + date + '\n'.join([
                f'{user_service.get_name_by_line_user_id(r[0])}: {"+" if r[1] > 0 else ""}{r[1]}'
                for r in sorted(
                    sum_hanchans.items(),
                    key=lambda x:x[1],
                    reverse=True
                )
            ])
        )
