from DomainService import (
    user_service,
    group_setting_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import (
    match_repository,
    hanchan_repository
)
from pymongo import DESCENDING


class ReplyApplyBadaiUseCase:

    def execute(self, badai: int) -> None:
        reply_service.add_message(
            '直前の対戦の最終会計を表示します。')

        badai = badai.replace(',', '')
        if not badai.isdigit():
            reply_service.add_message(
                ' 場代は自然数で入力してください。',
            )
            return
        badai = int(badai)

        line_group_id = request_info_service.req_line_group_id

        matches = match_repository.find(
            {
                'line_group_id': line_group_id,
                'status': 2,
            },
            {'created_at': DESCENDING},
        )
        if len(matches) == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return

        setting = group_setting_service.find_or_create(line_group_id)

        # TODO: 計算済みの結果カラムをMatchに追加する
        hanchans = hanchan_repository.find({'match_id': matches[0]._id})

        sum_hanchans = {}
        for i in range(len(hanchans)):
            converted_scores = hanchans[i].converted_scores

            for line_user_id, converted_score in converted_scores.items():
                if line_user_id not in sum_hanchans.keys():
                    sum_hanchans[line_user_id] = 0
                sum_hanchans[line_user_id] += converted_score

        player_count = len(sum_hanchans)
        badai_per_player = badai // player_count
        fraction = badai % player_count
        if fraction != 0:
            badai_per_player += 1
            fraction -= player_count

        tip_scores = matches[0].tip_scores
        show_prize_money_list = []
        rate = setting.rate * 10
        tip_rate = setting.tip_rate
        for line_user_id, converted_score in sum_hanchans.items():
            nullable_tip_count = tip_scores.get(line_user_id)
            tip_count = 0 if nullable_tip_count is None else nullable_tip_count
            
            price = converted_score * rate + tip_count * tip_rate - badai_per_player
            score = ("+" if converted_score > 0 else "") + str(converted_score)
            additional_tip_message = f'({("+" if tip_count > 0 else "") + str(tip_count)}枚)'
            show_prize_money_list.append(
                f'{user_service.get_name_by_line_user_id(line_user_id)}: {str(price)}円 ({score}{additional_tip_message})')

        str_fraction = '' if fraction == 0 else str(fraction) + '円'
        reply_service.add_message(
            '対戦ID: ' +
            str(matches[0]._id) +
            '\n' +
            f'場代: {badai}円({badai_per_player}円×{player_count}人{str_fraction})' +
            '\n' +
            '\n'.join(show_prize_money_list))
