from DomainService import (
    user_service,
    match_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from use_cases.utility.InputPointUseCase import InputPointUseCase


class AddTipByTextUseCase:

    def execute(
        self,
        text: str,
    ) -> None:
        line_group_id = request_info_service.req_line_group_id
        target_line_user_id, point = InputPointUseCase().execute(text)

        if point is None and target_line_user_id is None:
            return
        
        match = match_service.add_or_drop_tip_score(
            line_group_id=line_group_id,
            line_user_id=target_line_user_id,
            tip_score=point,
        )

        tips = match.tip_scores

        if len(tips) == 0:
            reply_service.add_message('チップを入力して下さい。')
            return
        
        res = [
            f'{user_service.get_name_by_line_user_id(line_user_id)}: {tip}'
            for line_user_id, tip in tips.items()
        ]

        reply_service.add_message("\n".join(res))
        return
