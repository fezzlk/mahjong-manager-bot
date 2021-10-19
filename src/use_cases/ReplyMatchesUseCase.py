from services import (
    request_info_service,
    reply_service,
    match_service,
)
import json


class ReplyMatchesUseCase:

    def execute(self) -> None:
        line_room_id = request_info_service.req_line_room_id
        matches = match_service.get_archived(line_room_id)
        if matches is None:
            reply_service.add_message(
                'まだ対戦結果がありません。'
            )
            return

        reply_service.add_message(
            '最近の4試合の結果を表示します。詳細は「_match <ID>」')
        for match in matches[:4]:
            self.reply_sum_and_money_by_ids(
                json.loads(match.result_ids),
                match._id,
                is_required_sum=False,
                date=match.created_at.strftime('%Y-%m-%d') + '\n'
            )
