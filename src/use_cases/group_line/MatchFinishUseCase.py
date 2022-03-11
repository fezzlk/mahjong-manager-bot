from DomainService import (
    user_service,
    match_service,
    config_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import session_scope, hanchan_repository


class MatchFinishUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        current_match = match_service.get_current(line_group_id=line_group_id)
        if current_match is None or len(current_match.hanchan_ids) == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return

        current = match_service.get_current(line_group_id)

        ids = current.hanchan_ids
        match_id = current._id

        with session_scope() as session:
            hanchans = hanchan_repository.find_by_ids(
                session, ids)

        sum_hanchans = {}
        for i in range(len(ids)):
            converted_scores = hanchans[i].converted_scores

            for line_user_id, converted_score in converted_scores.items():
                if line_user_id not in sum_hanchans.keys():
                    sum_hanchans[line_user_id] = 0
                sum_hanchans[line_user_id] += converted_score

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
            score = ("+" if converted_score > 0 else "") + str(converted_score)
            match_list.append(f'{name}: {price}円 ({score})')

        reply_service.add_message(
            '対戦ID: ' + str(match_id) + '\n' + '\n'.join(match_list)
        )

        match_service.archive(line_group_id)
