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
        line_group_id = request_info_service.req_line_group_id
        matches = match_service.get_archived(line_group_id)
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

                for line_user_id, converted_score in converted_scores.items():
                    if line_user_id not in sum_hanchans.keys():
                        sum_hanchans[line_user_id] = 0
                    sum_hanchans[line_user_id] += converted_score

            if is_required_sum:
                reply_service.add_message(
                    '\n'.join([
                        f'{user_service.get_name_by_line_user_id(line_user_id)}: {converted_score}'
                        for line_user_id, converted_score in sum_hanchans.items()
                    ])
                )

            key = 'レート'
            match_list = []
            for line_user_id, converted_score in sum_hanchans.items():
                name = user_service.get_name_by_line_user_id(line_user_id)
                price = str(
                    converted_score * int(config_service.get_value_by_key(line_group_id, key)[1]) * 10)
                score = ("+" if converted_score > 0 else "") + \
                    str(converted_score)
                match_list.append(f'{name}: {price}円 ({score})')

            reply_service.add_message(
                '対戦ID: ' +
                str(match_id) +
                '\n' +
                date +
                '\n' +
                '\n'.join(match_list))
