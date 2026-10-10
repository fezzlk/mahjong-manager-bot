from application_service import reply_service, request_info_service
from domain_model.entities.match_sum_session import MatchSumSession
from domain_service import match_service
from repositories import match_sum_session_repository


class StartSumMatchesUseCase:
    def execute(self) -> None:
        """_sum_matches: 直近10件の精算済み対戦から複数選択するセッションを開始する。"""
        line_group_id = request_info_service.req_line_group_id
        requester_line_id = request_info_service.req_line_user_id

        archived_matches = match_service.find_all_archived_by_line_group_id(line_group_id=line_group_id)
        if len(archived_matches) == 0:
            reply_service.add_message("まだ対戦結果がありません。")
            return

        match_sum_session_repository.create(
            MatchSumSession(
                line_group_id=line_group_id,
                requester_line_id=requester_line_id,
                selected_match_ids=[],
            ),
        )

        recent = archived_matches[-10:]
        start_index = len(archived_matches) - len(recent) + 1
        reply_service.add_message("合計を見たい対戦を選んでください（複数選択可、直近10件）。")
        reply_service.add_sum_matches_select_quick_reply(recent, start_index, [])
