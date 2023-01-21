from DomainModel.entities.Group import GroupMode
from DomainService import (
    user_service,
    match_service,
    config_service,
    group_service,
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

        tip_rate = int(config_service.get_value_by_key(line_group_id, 'チップ'))
        str_current_mode = group_service.get_mode(line_group_id).value
        if tip_rate != 0 and str_current_mode != GroupMode.tip_ok.value:
            group_service.chmod(line_group_id, GroupMode.tip_input)
            reply_service.add_message(
                'チップの増減数を入力してください。完了したら「_tip_ok」と入力してください。')
            return
        group_service.chmod(line_group_id, GroupMode.wait)

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

        tip_scores = current.tip_scores
        if tip_rate == 0:
            reply_service.add_message(
                '\n'.join([
                    f'{user_service.get_name_by_line_user_id(line_user_id)}: {converted_score}'
                    for line_user_id, converted_score in sum_hanchans.items()
                ])
            )
        else:
            show_sum_result_list = []
            for line_user_id, converted_score in sum_hanchans.items():
                nullable_tip_count = tip_scores.get(line_user_id)
                tip_count = 0 if nullable_tip_count is None else nullable_tip_count
                show_sum_result_list.append(
                    f'{user_service.get_name_by_line_user_id(line_user_id)}: {converted_score} ({tip_count}枚)')
            show_sum_result_message = '\n'.join(show_sum_result_list)
            reply_service.add_message(show_sum_result_message)

        show_prize_money_list = []
        for line_user_id, converted_score in sum_hanchans.items():
            name = user_service.get_name_by_line_user_id(line_user_id)
            rate = int(
                config_service.get_value_by_key(
                    line_group_id,
                    'レート')[1]
            ) * 10
            nullable_tip_count = tip_scores.get(line_user_id)
            tip_count = 0 if nullable_tip_count is None else nullable_tip_count
            price = converted_score * rate + tip_count * tip_rate
            score = ("+" if converted_score > 0 else "") + str(converted_score)
            additional_tip_message = f'({("+" if tip_count > 0 else "") + str(tip_count)}枚)'
            show_prize_money_list.append(
                f'{name}: {str(price)}円 ({score}{additional_tip_message})')

        reply_service.add_message(
            '対戦ID: ' + str(match_id) + '\n' + '\n'.join(show_prize_money_list)
        )

        match_service.archive(line_group_id)
