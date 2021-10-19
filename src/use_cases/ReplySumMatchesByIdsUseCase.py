from typing import List
from services import (
    reply_service,
    match_service,
)
import json


class ReplySumMatchesByIdsUseCase:

    def execute(self, ids: List[str]):
        formatted_id_list = sorted(list(set(ids)))
        matches = match_service.get(ids)
        if len(matches) == 0:
            reply_service.add_message(
                '該当する対戦結果がありません。'
            )
            return
        reply_service.add_message(
            f'対戦ID={",".join(formatted_id_list)}の累計を表示します。'
        )
        result_ids = []
        for match in matches:
            result_ids += json.loads(match.result_ids)
        self.reply_sum_and_money_by_ids(
            result_ids,
            ','.join(formatted_id_list),
            is_required_sum=False,
        )