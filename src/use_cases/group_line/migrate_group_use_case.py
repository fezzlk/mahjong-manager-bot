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

    def execute_personal(self) -> None:
        """_personal_migrate: 個人DMからの統合操作（パラメータで3ステップ分岐）。

        params なし         → Step 1: 統合元グループ選択 QR
        src=<id> のみ       → Step 2: 統合先グループ選択 QR
        src=<id>&to=<id>   → Step 3: 統合確定
        """
        req_line_user_id = request_info_service.req_line_user_id
        src_param = request_info_service.params.get("src")
        to_param = request_info_service.params.get("to")

        if src_param and to_param:
            self._personal_confirm(req_line_user_id, src_param, to_param)
        elif src_param:
            self._personal_select_dest(req_line_user_id, src_param)
        else:
            self._personal_select_src(req_line_user_id)

    def _personal_select_src(self, line_user_id: str) -> None:
        user_groups = user_group_repository.find({"line_user_id": line_user_id})
        group_ids = [ug.line_group_id for ug in user_groups]
        sources = group_repository.find({
            "line_group_id": {"$in": group_ids},
            "merged_into": None,
        })
        if len(sources) < 2:
            reply_service.add_message("統合できるグループが2つ以上必要です。")
            return
        reply_service.add_personal_migrate_source_quick_reply(sources)

    def _personal_select_dest(self, line_user_id: str, src_group_id: str) -> None:
        src_groups = group_repository.find({"line_group_id": src_group_id})
        if not src_groups:
            reply_service.add_message("指定された統合元グループが存在しません。")
            return

        user_groups = user_group_repository.find({"line_user_id": line_user_id})
        candidate_ids = [
            ug.line_group_id for ug in user_groups
            if ug.line_group_id != src_group_id
        ]
        dests = group_repository.find({
            "line_group_id": {"$in": candidate_ids},
            "merged_into": None,
        })
        if not dests:
            reply_service.add_message("統合先グループが見つかりません。")
            return

        src_name = src_groups[0].group_name or src_group_id
        reply_service.add_message(f"「{src_name}」の統合先を選んでください。")
        reply_service.add_personal_migrate_dest_quick_reply(dests, src_group_id)

    def _personal_confirm(
        self, line_user_id: str, src_group_id: str, to_group_id: str
    ) -> None:
        targets = group_repository.find({"line_group_id": to_group_id})
        if not targets:
            reply_service.add_message("統合先グループが存在しません。")
            return

        group_service.set_merged_into(src_group_id, to_group_id)
        dest_name = targets[0].group_name or to_group_id
        reply_service.add_message(
            f"統合しました。\n"
            f"今後「{dest_name}」でまとめて成績を確認できます。",
        )
