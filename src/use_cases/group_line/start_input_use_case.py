from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import GroupMode
from domain_service import (
    group_service,
    hanchan_service,
    match_service,
)


class StartInputUseCase:
    def execute(self) -> None:
        group = group_service.find_one_by_line_group_id(
            request_info_service.req_line_group_id,
        )

        if group is None:
            reply_service.add_message(
                "トークルームが登録されていません。招待し直してください。",
            )
            return
        if group.mode == GroupMode.input.value:
            reply_service.add_message("すでに入力モードです。")
            return

        # sim モードからの切り替え時は sim 用半荘をクリーンアップ
        if group.mode == GroupMode.sim.value:
            self._cleanup_sim_hanchan(group)

        # group の active match を取得、なければ作成
        active_match = match_service.find_one_by_id(group.active_match_id)
        if active_match is None:
            active_match = match_service.create_with_line_group_id(group.line_group_id)
            group.active_match_id = active_match._id

        # match の active hanchan を取得、なければ作成
        active_hanchan = hanchan_service.find_one_by_id(active_match.active_hanchan_id)
        if active_hanchan is None:
            active_hanchan = hanchan_service.create_with_line_group_id_and_match_id(
                group.line_group_id, active_match._id,
            )
            active_match.active_hanchan_id = active_hanchan._id
            match_service.update(active_match)

        group.mode = GroupMode.input.value
        group_service.update(group)

        hanchans = hanchan_service.find_all_archived_by_match_id(active_match._id)
        reply_service.add_message(
            f"第{len(hanchans) + 1}回戦お疲れ様です。各自点数を入力してください。\n(同点の場合は上家が高くなるように数点追加してください)",
        )

    @staticmethod
    def _cleanup_sim_hanchan(group) -> None:
        """sim モードの半荘を削除し、active_hanchan_id をリセットする。"""
        active_match = match_service.find_one_by_id(group.active_match_id)
        if active_match is None:
            return
        sim_hanchan = hanchan_service.find_one_by_id(active_match.active_hanchan_id)
        if sim_hanchan is not None:
            sim_hanchan.is_deleted = True
            hanchan_service.update(sim_hanchan)
        active_match.active_hanchan_id = None
        match_service.update(active_match)
