from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainService import (
    group_service,
    match_service,
    user_service,
)
from use_cases.utility.InputPointUseCase import InputPointUseCase


class AddChipByTextUseCase:
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
                "グループが登録されていません。招待し直してください。",
            )
            return
        active_match = match_service.find_one_by_id(group.active_match_id)
        if active_match is None:
            reply_service.add_message(
                "計算対象の試合が見つかりません。",
            )
            return
        match = match_service.add_or_drop_chip_score(
            match_id=active_match._id,
            line_user_id=target_line_user_id,
            chip_score=point,
        )

        chips = match.chip_scores

        if len(chips) == 0:
            reply_service.add_message("チップの増減枚数を入力して下さい。")
            return

        res = [
            f"{user_service.get_name_by_line_user_id(line_user_id) or '友達未登録'}: {chip}"
            for line_user_id, chip in chips.items()
        ]

        reply_service.add_message("\n".join(res))
        return
