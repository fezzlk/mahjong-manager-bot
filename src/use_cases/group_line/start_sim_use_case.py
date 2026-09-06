from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import GroupMode
from domain_model.entities.match import Match, MatchStatus
from domain_service import (
    group_service,
    hanchan_service,
    match_service,
)
from repositories import match_repository


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

        # sim専用の使い捨てサンドボックスを取得、なければ作成。
        # 実系列のactive_match_idとは独立させることで、実対戦の入力中に
        # _simを実行しても実データを上書きしないようにする。status=sim
        # を明示することで、find_latest_one等の実対戦検索から常に除外される。
        sim_match = match_service.find_one_by_id(group.sim_match_id)
        if sim_match is None:
            sim_match = Match(
                line_group_id=group.line_group_id,
                status=MatchStatus.sim.value,
            )
            match_repository.create(sim_match)
            group.sim_match_id = sim_match._id

        # sim 用に常に新しい半荘を作成（既存の input 半荘データが混入しないようにする）
        sim_hanchan = hanchan_service.create_with_line_group_id_and_match_id(
            group.line_group_id, sim_match._id,
        )
        sim_match.active_hanchan_id = sim_hanchan._id
        match_service.update(sim_match)

        group.mode = GroupMode.sim.value
        group_service.update(group)

        reply_service.add_message(
            "[シミュレーション] 各自点数を入力してください。\n(結果は記録されません)",
        )
