from DomainModel.entities.Group import GroupMode
from DomainService import (
    group_service,
    match_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from use_cases.group_line.FinishMatchUseCase import FinishMatchUseCase


class FinishInputTipUseCase:

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
        sum_tip_count = 0
        for tip in active_match.tip_scores.values():
            sum_tip_count += tip

        if sum_tip_count != 0:
            reply_service.add_message(
                f'チップ増減数の合計が{("+" if sum_tip_count > 0 else "") + str(sum_tip_count)}です。0になるようにしてください。）'
            )
            return

        group_service.chmod(line_group_id, GroupMode.tip_ok)
        FinishMatchUseCase().execute()
