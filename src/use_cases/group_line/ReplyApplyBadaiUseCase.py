from DomainService import (
    user_service,
    config_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import (
    session_scope,
    match_repository,
    hanchan_repository
)


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

        with session_scope() as session:
            matches = match_repository.find_many_by_line_group_id_and_status(
                session=session,
                line_group_id=line_group_id,
                status=2
            )
        if matches is None or len(matches) == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return

        current = sorted(matches, key=lambda x: x.created_at, reverse=True)[0]
        tip_rate = int(config_service.get_value_by_key(line_group_id, 'チップ'))

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

        player_count = len(sum_hanchans)
        badai_per_player = badai // player_count
        fraction = badai % player_count
        if fraction != 0:
            badai_per_player += 1
            fraction -= player_count

        tip_scores = current.tip_scores
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
            price = converted_score * rate + tip_count * tip_rate - badai_per_player
            score = ("+" if converted_score > 0 else "") + str(converted_score)
            additional_tip_message = f'({("+" if tip_count > 0 else "") + str(tip_count)}枚)'
            show_prize_money_list.append(
                f'{name}: {str(price)}円 ({score}{additional_tip_message})')

        str_fraction = '' if fraction == 0 else str(fraction) + '円'
        reply_service.add_message(
            '対戦ID: ' +
            str(match_id) +
            '\n' +
            f'場代: {badai}円({badai_per_player}円×{player_count}人{str_fraction})' +
            '\n' +
            '\n'.join(show_prize_money_list))
