from typing import Optional

from bson.errors import InvalidId
from bson.objectid import ObjectId

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.match import Match, MatchStatus
from domain_service import (
    group_service,
    hanchan_service,
    match_service,
)


class StartInputUseCase:
    """点数入力モードを開始する。

    グループは複数の対戦を同時にopenで持てる(FEZ-66 Phase E)ため、open対戦が
    2件以上ならピッカーで対象を選ばせる(「新しい対戦を始める」項目は_new_match
    へ合流する)。0件・1件の場合は従来通り黙って続行する(頻度の高い単一系列の
    利用に余計な手間を増やさないため)。
    """

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

        open_matches = match_service.find_all_open_by_line_group_id(group.line_group_id)
        if len(open_matches) == 0:
            self.enter_match(group, None)
            return
        if len(open_matches) == 1:
            self.enter_match(group, open_matches[0])
            return

        reply_service.add_input_target_quick_reply(open_matches)

    def select(self) -> None:
        """_input_select?to=<match_id>: ピッカーで選択された対戦の入力を開始する。"""
        line_group_id = request_info_service.req_line_group_id
        match_id = request_info_service.params.get("to")
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "トークルームが登録されていません。招待し直してください。",
            )
            return
        if group.mode == GroupMode.input.value:
            reply_service.add_message("すでに入力モードです。")
            return

        if not match_id:
            reply_service.add_message("入力を始める対戦が指定されていません。")
            return

        try:
            target_match = match_service.find_one_by_id(ObjectId(match_id))
        except InvalidId:
            target_match = None
        if (
            target_match is None
            or target_match.line_group_id != line_group_id
            or target_match.status != MatchStatus.open.value
        ):
            reply_service.add_message("指定された対戦が見つかりません。")
            return

        self.enter_match(group, target_match)

    def enter_match(self, group: Group, match: Optional[Match]) -> None:
        """指定対戦(matchがNoneなら新規作成)への入力を開始する。

        `_new_match`(NewMatchUseCase)からも新規対戦作成後の入力開始として
        呼ばれる。matchがNoneの場合の新規作成はmode更新の"後"に行う——
        点数入力が_inputコマンドと同時に送られた場合でも並行ワーカーが
        inputモードを認識できるよう、対戦作成(やや時間のかかるDB書き込み)
        より先にmodeだけを素早く更新するため(既存のレース条件対策を維持)。
        """
        original_mode = group.mode

        group.mode = GroupMode.input.value
        group_service.update(group)

        # sim モードからの切り替え時は sim 用半荘をクリーンアップ
        if original_mode == GroupMode.sim.value:
            self._cleanup_sim_hanchan(group)

        if match is None:
            match = match_service.create_with_line_group_id(
                group.line_group_id,
                settings=group_service.get_settings_or_create(group.line_group_id),
            )

        group.current_input_match_id = match._id
        group_service.update(group)

        # match の active hanchan を取得、なければ作成
        active_hanchan = hanchan_service.find_one_by_id(match.active_hanchan_id)
        if active_hanchan is None:
            active_hanchan = hanchan_service.create_with_line_group_id_and_match_id(
                group.line_group_id, match._id,
            )
            match.active_hanchan_id = active_hanchan._id
            match_service.update(match)

        hanchans = hanchan_service.find_all_archived_by_match_id(match._id)
        reply_service.add_message(
            f"第{len(hanchans) + 1}回戦お疲れ様です。各自点数を入力してください。\n(同点の場合は上家が高くなるように数点追加してください)",
        )

    @staticmethod
    def _cleanup_sim_hanchan(group) -> None:
        """Simモード専用サンドボックス(sim_match_id)の半荘を削除し、active_hanchan_idをリセットする。

        sim_match_idは実系列のcurrent_input_match_idとは独立しているため、ここで
        実系列のデータに触れることはない。
        """
        sim_match = match_service.find_one_by_id(group.sim_match_id)
        if sim_match is None:
            return
        sim_hanchan = hanchan_service.find_one_by_id(sim_match.active_hanchan_id)
        if sim_hanchan is not None:
            sim_hanchan.is_deleted = True
            hanchan_service.update(sim_hanchan)
        sim_match.active_hanchan_id = None
        match_service.update(sim_match)
