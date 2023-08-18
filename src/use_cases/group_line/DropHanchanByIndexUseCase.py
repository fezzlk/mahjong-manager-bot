from DomainService import (
    match_service,
    group_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import (
    hanchan_repository,
)
from pymongo import ASCENDING


class DropHanchanByIndexUseCase:

    def execute(self, i: int) -> None:
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
                'まだ対戦結果がありません。'
            )
            return
        hanchans = hanchan_repository.find(
            {'match_id': active_match._id},
            [('_id', ASCENDING)])
        
        hanchan_repository.update(
            {'_id': hanchans[i - 1]._id},
            {'status': 0},
        )

        reply_service.add_message(
            f'現在の対戦の第{i}半荘の結果を削除しました。'
        )
