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
from typing import Dict


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
        if tip_rate != 0 and group_service.get_mode(line_group_id) != GroupMode.tip_ok.value:
            group.mode = GroupMode.tip_input.value
            group_service.update(group)
            reply_service.add_message(
                'チップの増減数を入力してください。完了したら「_tip_ok」と入力してください。')
            return
        

        # 精算
        rate = settings.rate * 10
        sum_scores = active_match.sum_scores
        tip_scores = active_match.tip_scores

        tip_prices: Dict[str, int] = {}
        sum_prices: Dict[str, int] = {}
        sum_prices_with_tip: Dict[str, int] = {}
        for line_user_id, converted_score in sum_scores.items():
            if tip_scores.get(line_user_id) is None:
                tip_score = 0
                tip_scores[line_user_id] = 0
            else:
                tip_score = tip_scores.get(line_user_id)

            tip_price = tip_score * tip_rate
            tip_prices[line_user_id] = tip_price

            price = converted_score * rate
            sum_prices[line_user_id] = price

            sum_prices_with_tip[line_user_id] = price + tip_price

        # 試合のアーカイブ
        active_match.tip_prices = tip_prices
        active_match.sum_prices = sum_prices
        active_match.sum_prices_with_tip = sum_prices_with_tip
        match_service.update(active_match)
        group.mode = GroupMode.wait.value
        group.active_match_id = None
        group_service.update(group)

        # 応答メッセージ作成
        show_prize_money_list = []
        for line_user_id, converted_score in sum_scores.items():
            name = user_service.get_name_by_line_user_id(line_user_id)
            price = sum_prices_with_tip[line_user_id]
            score = ("+" if converted_score > 0 else "") + str(converted_score)
            tip_score = tip_scores[line_user_id]
            additional_tip_message = f'({("+" if tip_score > 0 else "") + str(tip_score)}枚)'
            
            show_prize_money_list.append(
                f'{name}: {str(price)}円 ({score}{additional_tip_message})')

        reply_service.add_message(
            '対戦結果: \n' + '\n'.join(show_prize_money_list)
        )
