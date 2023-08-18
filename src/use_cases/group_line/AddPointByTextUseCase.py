from DomainService import (
    user_service,
    hanchan_service,
    group_service,
    match_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from use_cases.group_line.SubmitHanchanUseCase import SubmitHanchanUseCase
from use_cases.utility.InputPointUseCase import InputPointUseCase


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
        
        # Active 半荘を取得し点数を追加
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        active_match = match_service.find_one_by_id(group.active_match_id)
        hanchan = hanchan_service.add_or_drop_raw_score(
            hanchan_id=active_match.active_hanchan_id,
            line_user_id=target_line_user_id,
            raw_score=point,
        )

        raw_scores = hanchan.raw_scores

        # 応答メッセージ作成
        if len(raw_scores) == 0:
            reply_service.add_message('点数を入力してください。')
            return

        res = [
            f'{user_service.get_name_by_line_user_id(line_user_id)}: {raw_score}'
            for line_user_id, raw_score in raw_scores.items()
        ]

        reply_service.add_message("\n".join(res))

        if len(raw_scores) == 4:
            SubmitHanchanUseCase().execute()
        elif len(raw_scores) > 4:
            reply_service.add_message(
                '5人以上入力されています。@[ユーザー名] で不要な入力を消してください。'
            )

        return
