from DomainModel.entities.Group import GroupMode
from DomainService import (
    user_service,
    match_service,
    group_service,
    group_setting_service,
    hanchan_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)


class FinishMatchUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                'グループが登録されていません。招待し直してください。'
            )
            return

        active_match = match_service.find_one_by_id(group.active_match_id)
        if active_match is None:
            reply_service.add_message(
                '計算対象の試合が見つかりません。'
            )
            return
        
        hanchans = hanchan_service.find_all_by_match_id(active_match._id)

        if len(hanchans) == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return

        settings = group_setting_service.find_or_create(request_info_service.req_line_group_id)
        tip_rate = settings.tip_rate
        str_current_mode = group_service.get_mode(line_group_id)
        if tip_rate != 0 and str_current_mode != GroupMode.tip_ok.value:
            group.mode = GroupMode.tip_input.value
            group_service.update(group)
            reply_service.add_message(
                'チップの増減数を入力してください。完了したら「_tip_ok」と入力してください。')
            return
        
        # 試合のアーカイブ
        group.mode = GroupMode.wait.value
        group.active_match_id = None
        group_service.update(group)

        # 応答メッセージの作成
        sum_hanchans = {}
        for h in hanchans:
            converted_scores = h.converted_scores

            for line_user_id, converted_score in converted_scores.items():
                if line_user_id not in sum_hanchans.keys():
                    sum_hanchans[line_user_id] = 0
                sum_hanchans[line_user_id] += converted_score

        tip_scores = active_match.tip_scores

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
            '対戦ID: ' + str(active_match._id) + '\n' + '\n'.join(show_prize_money_list)
        )

