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


class StartSimUseCase:
    def execute(self) -> None:
        group = group_service.find_one_by_line_group_id(
            request_info_service.req_line_group_id,
        )

        if group is None:
            reply_service.add_message(
                "トークルームが登録されていません。招待し直してください。",
            )
            return
        if group.mode == GroupMode.sim.value:
            reply_service.add_message("すでにシミュレーションモードです。")
            return

        # group の active match を取得、なければ作成
        active_match = match_service.find_one_by_id(group.active_match_id)
        if active_match is None:
            active_match = match_service.create_with_line_group_id(group.line_group_id)
            group.active_match_id = active_match._id

        # sim 用に常に新しい半荘を作成（既存の input 半荘データが混入しないようにする）
        sim_hanchan = hanchan_service.create_with_line_group_id_and_match_id(
            group.line_group_id, active_match._id,
        )
        active_match.active_hanchan_id = sim_hanchan._id
        match_service.update(active_match)

        group.mode = GroupMode.sim.value
        group_service.update(group)

        reply_service.add_message(
            "[シミュレーション] 各自点数を入力してください。\n(結果は記録されません)",
        )
