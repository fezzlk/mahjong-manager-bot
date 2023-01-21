from DomainModel.entities.Group import GroupMode
from DomainService import (
    group_service,
    match_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from use_cases.group_line.MatchFinishUseCase import MatchFinishUseCase


class FinishInputTipUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        current = match_service.get_current(line_group_id)
        sum_tip_count = 0
        for tip in current.tip_scores.values():
            sum_tip_count += tip

        if sum_tip_count != 0:
            reply_service.add_message(
                f'チップ増減数が{sum_tip_count}です。0になるようにしてください。（中断する場合は「_exit」）'
            )
            return

        group_service.chmod(line_group_id, GroupMode.tip_ok)
        MatchFinishUseCase().execute()
