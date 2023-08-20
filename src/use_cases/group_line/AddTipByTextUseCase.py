from DomainService import (
    user_service,
    match_service,
    group_service,
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
        match = match_service.add_or_drop_tip_score(
            match_id=active_match._id,
            line_user_id=target_line_user_id,
            tip_score=point,
        )

        tips = match.tip_scores

        if len(tips) == 0:
            reply_service.add_message('チップを入力して下さい。')
            return
        
        res = [
            f'{user_service.get_name_by_line_user_id(line_user_id) or "友達未登録"}: {tip}'
            for line_user_id, tip in tips.items()
        ]

        reply_service.add_message("\n".join(res))
        return
