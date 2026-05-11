from application_service import (
    reply_service,
    request_info_service,
)
from domain_service import group_service
from repositories import (
    group_repository,
    user_group_repository,
)


class MigrateGroupUseCase:
    def execute(self) -> None:
        """_migrate: 統合先グループの選択 Quick Reply を表示する。"""
        src_group_id = request_info_service.req_line_group_id
        req_line_user_id = request_info_service.req_line_user_id

        user_groups = user_group_repository.find({"line_user_id": req_line_user_id})
        candidate_ids = [
            ug.line_group_id for ug in user_groups
            if ug.line_group_id != src_group_id
        ]
        if not candidate_ids:
            reply_service.add_message("統合先グループが見つかりません。")
            return

        candidates = group_repository.find({
            "line_group_id": {"$in": candidate_ids},
            "merged_into": None,
        })
        if not candidates:
            reply_service.add_message("統合先グループが見つかりません。")
            return

        reply_service.add_migrate_target_quick_reply(candidates)

    def confirm(self) -> None:
        """_migrate_confirm?to=<line_group_id>: 統合を確定する。"""
        src_group_id = request_info_service.req_line_group_id
        to_group_id = request_info_service.params.get("to")

        if not to_group_id:
            reply_service.add_message("統合先が指定されていません。")
            return

        targets = group_repository.find({"line_group_id": to_group_id})
        if not targets:
            reply_service.add_message("統合先グループが存在しません。")
            return

        group_service.set_merged_into(src_group_id, to_group_id)
        dest_name = targets[0].group_name or to_group_id
        reply_service.add_message(
            f"このグループの成績を「{dest_name}」に統合しました。\n"
            "今後このグループの成績は統合先でまとめて確認できます。",
        )
