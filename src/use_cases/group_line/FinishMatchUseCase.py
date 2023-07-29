from DomainModel.entities.Group import GroupMode
from DomainService import (
    user_service,
    match_service,
    group_service,
    group_setting_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import hanchan_repository


class FinishMatchUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        current_match = match_service.get_current(line_group_id=line_group_id)
        if current_match is None:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return
        
        hanchans = hanchan_repository.find({
            'match_id': current_match._id,
            'line_group_id': request_info_service.req_line_group_id,
            'status': 2,
        })

        if len(hanchans) == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return

        settings = group_setting_service.find_or_create(request_info_service.req_line_group_id)
        tip_rate = settings.tip_rate
        str_current_mode = group_service.get_mode(line_group_id)
        if tip_rate != 0 and str_current_mode != GroupMode.tip_ok.value:
            group_service.chmod(line_group_id, GroupMode.tip_input)
            reply_service.add_message(
                'チップの増減数を入力してください。完了したら「_tip_ok」と入力してください。')
            return
        group_service.chmod(line_group_id, GroupMode.wait)

        sum_hanchans = {}
        for h in hanchans:
            converted_scores = h.converted_scores

            for line_user_id, converted_score in converted_scores.items():
                if line_user_id not in sum_hanchans.keys():
                    sum_hanchans[line_user_id] = 0
                sum_hanchans[line_user_id] += converted_score

        tip_scores = current_match.tip_scores

        rate = settings.rate * 10
        show_prize_money_list = []
        for line_user_id, converted_score in sum_hanchans.items():
            name = user_service.get_name_by_line_user_id(line_user_id)
            nullable_tip_count = tip_scores.get(line_user_id)
            tip_count = 0 if nullable_tip_count is None else nullable_tip_count
            price = converted_score * rate + tip_count * tip_rate
            score = ("+" if converted_score > 0 else "") + str(converted_score)
            additional_tip_message = f'({("+" if tip_count > 0 else "") + str(tip_count)}枚)'
            show_prize_money_list.append(
                f'{name}: {str(price)}円 ({score}{additional_tip_message})')

        reply_service.add_message(
            '対戦ID: ' + str(current_match._id) + '\n' + '\n'.join(show_prize_money_list)
        )

        match_service.update_status_active_match(line_group_id, 2)
