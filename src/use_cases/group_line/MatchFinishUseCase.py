from typing import Dict, List
from DomainService import (
    user_service,
    match_service,
    config_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import (
    session_scope,
    hanchan_repository,
    yakuman_user_repository,
)


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
            yakuman_users = yakuman_user_repository.find_by_hanchan_ids(
                session, ids)

        total_scores: Dict[str, int] = {}
        total_yakuman_plus: Dict[str, int] = {
            k: 0 for k in total_scores.keys()}
        total_yakuman_minus: Dict[str, int] = {
            k: 0 for k in total_scores.keys()}

        for hanchan in hanchans:
            converted_scores = hanchan.converted_scores

            for line_user_id, converted_score in converted_scores.items():
                if line_user_id not in total_scores.keys():
                    total_scores[line_user_id] = 0
                total_scores[line_user_id] += converted_score

            for yu in [
                    target for target in yakuman_users if target.hanchan_id == hanchan._id]:
                for line_user_id in converted_scores.keys():
                    if line_user_id == yu.user_id:
                        total_yakuman_plus[line_user_id] += 1
                    else:
                        total_yakuman_minus[line_user_id] += 1

        results: List[str] = []
        for line_user_id, converted_score in total_scores.items():
            yakuman_info = '+' * total_yakuman_plus[line_user_id] \
                + '-' * total_yakuman_minus[line_user_id]
            results.append(
                f'{user_service.get_name_by_line_user_id(line_user_id)}: {converted_score}{yakuman_info}')

        reply_service.add_message(
            '\n'.join(results)
        )

        price_list = []
        for line_user_id, converted_score in total_scores.items():
            name = user_service.get_name_by_line_user_id(line_user_id)
            rate = int(
                config_service.get_value_by_key(
                    line_group_id, 'レート')[1])
            yakuman_prize = 300
            price = str(converted_score * rate * 10)\
                + yakuman_prize * 3 * total_yakuman_plus[line_user_id]\
                - yakuman_prize * total_yakuman_minus[line_user_id]
            yakuman_info = '+' * total_yakuman_plus[line_user_id]\
                + '-' * total_yakuman_minus[line_user_id]
            score = ("+" if converted_score > 0 else "") + \
                str(converted_score) + yakuman_info
            price_list.append(f'{name}: {price}円 ({score})')

        reply_service.add_message(
            '対戦ID: ' + str(match_id) + '\n' + '\n'.join(price_list)
        )

        match_service.archive(line_group_id)
