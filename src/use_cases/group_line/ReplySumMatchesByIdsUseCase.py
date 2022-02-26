from typing import List
from DomainService import (
    hanchan_service,
    user_service,
    config_service,
)

from ApplicationService import (
    reply_service,
    request_info_service,
)
from repositories import session_scope, match_repository


class ReplySumMatchesByIdsUseCase:

    def execute(self, ids: List[str]) -> None:
        formatted_id_list = sorted(list(set(ids)))
        with session_scope() as session:
            matches = match_repository.find_by_ids(session=session, ids=ids)
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
            line_group_id = request_info_service.req_line_group_id
            for line_user_id, converted_score in sum_hanchans.items():
                name = user_service.get_name_by_line_user_id(line_user_id)
                price = str(
                    converted_score * int(config_service.get_value_by_key(line_group_id, key)[1]) * 10)
                score = ("+" if converted_score > 0 else "") + \
                    str(converted_score)
                match_list.append(f'{name}: {price}円 ({score})')

            reply_service.add_message(
                '対戦ID: ' + str(match_id) + '\n' + date + '\n'.join(match_list)
            )
