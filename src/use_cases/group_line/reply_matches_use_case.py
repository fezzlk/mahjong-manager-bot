from application_service import (
    reply_service,
    request_info_service,
)
from domain_service import match_service


class ReplyMatchesUseCase:
    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        archived_matches = match_service.find_all_archived_by_line_group_id(line_group_id=line_group_id)

        if len(archived_matches) == 0:
            reply_service.add_message(
                "まだ対戦結果がありません。",
            )
            return

        reply_service.add_message(
            "このトークルームで行われた対戦一覧を表示します。第N回の詳細は「_match N」と送ってください。")

        # 複数系列を実際に使ったことがあるグループのみ対戦名を表示する
        # (単一系列グループでは無用な表示になるため。FEZ-66 Phase F)
        show_name = match_service.count_non_sim_by_line_group_id(line_group_id) > 1
        match_details = []
        for i, match in enumerate(archived_matches):
            date_str = match.created_at.strftime("%Y-%m-%d")
            if show_name:
                match_details.append(f"第{i+1}回 {date_str}「{match.name or match._id}」")
            else:
                match_details.append(f"第{i+1}回 {date_str}")

        reply_service.add_message("\n".join(match_details))
