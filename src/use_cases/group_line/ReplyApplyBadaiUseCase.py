from ApplicationService import (
    request_info_service,
    reply_service,
)
from DomainService import (
    user_service,
)
from repositories import (
    match_repository,
)
from pymongo import DESCENDING


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

        matches = match_repository.find(
            {
                'line_group_id': line_group_id,
                'status': 2,
            },
            [('created_at', DESCENDING)],
        )
        if len(matches) == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return

        player_count = len(matches[0].sum_prices_with_tip)

        badai_per_player = badai // player_count
        fraction = badai % player_count
        if fraction != 0:
            badai_per_player += 1
            fraction -= player_count
        str_fraction = '' if fraction == 0 else str(fraction) + '円'

        str_each_price = []
        for u_id, p in matches[0].sum_prices_with_tip.items():
            name = user_service.get_name_by_line_user_id(u_id) or "友達未登録"
            str_each_price.append(f'{name}: {p - badai_per_player}円')

        reply_service.add_message(
            '直前の対戦の最終会計を表示します。')
        reply_service.add_message(
            '対戦ID: ' +
            str(matches[0]._id) +
            '\n' +
            f'場代: {badai}円({badai_per_player}円×{player_count}人{str_fraction})' +
            '\n' +
            '\n'.join(str_each_price)
        )
