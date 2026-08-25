from application_service import (
    reply_service,
    request_info_service,
)
from domain_service import (
    group_service,
    group_setting_service,
    hanchan_service,
    match_service,
    user_service,
)
from use_cases.group_line.submit_hanchan_use_case import SubmitHanchanUseCase
from use_cases.utility.input_point_use_case import InputPointUseCase


class AddPointByTextUseCase:

    def execute(
        self,
        text: str,
    ) -> None:
        line_group_id = request_info_service.req_line_group_id

        # メーセージから対象ユーザと点数の取得
        target_line_user_id, point = InputPointUseCase().execute(text)
        if point is None and target_line_user_id is None:
            return

        # 現在入力中の半荘を取得し点数を追加
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message("グループが登録されていません。招待し直してください。")
            return
        active_match = match_service.find_one_by_id(group.active_match_id)
        if active_match.active_hanchan_id is None:
            return
        hanchan = hanchan_service.add_or_drop_raw_score(
            hanchan_id=active_match.active_hanchan_id,
            line_user_id=target_line_user_id,
            raw_score=point,
        )

        raw_scores = hanchan.raw_scores

        # 応答メッセージ作成
        if len(raw_scores) == 0:
            reply_service.add_message("点数を入力してください。")
            return

        res = [
            f'{user_service.get_name_by_line_user_id(line_user_id) or "友達未登録"}: {raw_score}'
            for line_user_id, raw_score in raw_scores.items()
        ]

        reply_service.add_message("\n".join(res))

        num_of_players = group_setting_service.find_or_create(line_group_id).num_of_players
        if len(raw_scores) == num_of_players:
            SubmitHanchanUseCase().execute()
        elif len(raw_scores) > num_of_players:
            reply_service.add_message(
                f"{num_of_players + 1}人以上入力されています。@[ユーザー名] で不要な入力を消してください。",
            )

        return
