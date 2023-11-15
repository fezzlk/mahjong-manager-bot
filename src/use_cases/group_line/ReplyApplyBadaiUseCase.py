from ApplicationService import (
    request_info_service,
    reply_service,
)
from DomainService import (
    user_service,
    match_service,
)


class ReplyApplyBadaiUseCase:

    def execute(self, badai: str) -> None:

        badai = badai.replace(',', '')
        if not badai.isdigit():
            reply_service.add_message(
                '場代は自然数で入力してください。',
            )
            return
        badai = int(badai)

        line_group_id = request_info_service.req_line_group_id

        latest_match = match_service.find_latest_one(line_group_id=line_group_id)

        if latest_match is None:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return

        if latest_match.sum_prices_with_tip is None or len(latest_match.sum_prices_with_tip) == 0:
            reply_service.add_message(
                '現在進行中の対戦があります。対戦を終了するには「_finish」と送信してください。')
            return
        
        player_count = len(latest_match.sum_prices_with_tip)

        badai_per_player = badai // player_count
        fraction = badai % player_count
        if fraction != 0:
            badai_per_player += 1
            fraction -= player_count
        str_fraction = '' if fraction == 0 else str(fraction) + '円'

        str_each_price = []
        for u_id, p in latest_match.sum_prices_with_tip.items():
            name = user_service.get_name_by_line_user_id(u_id) or "友達未登録"
            str_each_price.append(f'{name}: {p - badai_per_player}円')

        reply_service.add_message(
            '直前の対戦の最終会計を表示します。')
        reply_service.add_message(
            '対戦開始日: ' +
            latest_match.created_at.strftime("%Y年%m月%d日") +
            '\n' +
            f'場代: {badai}円({badai_per_player}円×{player_count}人{str_fraction})' +
            '\n' +
            '\n'.join(str_each_price)
        )
