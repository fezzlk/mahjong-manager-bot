import logging
from typing import Dict, Optional

from bson.errors import InvalidId
from bson.objectid import ObjectId

from application_service import (
    message_service,
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.match import Match, MatchStatus
from domain_service import (
    group_service,
    group_setting_service,
    hanchan_service,
    match_service,
)
from use_cases.group_line.create_match_detail_graph_use_case import (
    CreateMatchDetailGraphUseCase,
)

logger = logging.getLogger(__name__)


class FinishMatchUseCase:
    """対戦(半荘の集合)を精算する。

    グループは複数の対戦を同時にopenで持てる(FEZ-66 Phase D/E)ため、
    `_finish`はopen対戦が2件以上ならピッカーで対象を選ばせ、1件なら
    従来通り即座に精算する。0件なら「見つかりません」。
    """

    def execute(self) -> None:
        """_finish: open対戦数に応じて即精算 or ピッカー提示。"""
        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return

        open_matches = match_service.find_all_open_by_line_group_id(line_group_id)
        if len(open_matches) == 0:
            reply_service.add_message(
                "計算対象の試合が見つかりません。",
            )
            return
        if len(open_matches) == 1:
            self._settle(group, open_matches[0])
            return

        reply_service.add_finish_target_quick_reply(open_matches)

    def select(self) -> None:
        """_finish_select?to=<match_id>: ピッカーで選択された対戦を精算する。"""
        line_group_id = request_info_service.req_line_group_id
        match_id = request_info_service.params.get("to")
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return

        if not match_id:
            reply_service.add_message("精算する対戦が指定されていません。")
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

        self._settle(group, target_match)

    def finish_pending_chip(self) -> None:
        """_chip_ok経由: チップ入力完了後の二段階目の精算を行う。

        由来の対戦は必ずcurrent_input_match_idが指すそれ自身(チップ入力
        セッションを開始したのはこの対戦のexecute()/select()自身)なので、
        ここではopen対戦数による分岐は不要。
        """
        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return

        active_match = match_service.find_one_by_id(group.current_input_match_id)
        if active_match is None:
            reply_service.add_message(
                "計算対象の試合が見つかりません。",
            )
            return

        self._settle(group, active_match)

    def _settle(self, group: Group, active_match: Match) -> None:
        line_group_id = group.line_group_id

        # 複数対戦が同時にopenな状況で、別の対戦が入力セッション中
        # (current_input_match_idがこの対戦以外を指す)場合は精算をブロックする。
        # 放置すると精算処理(group.mode書き換え等)が他対戦の入力セッションを
        # 無警告で壊してしまう(FEZ-66 Phase E)。
        other_session_match_id: Optional[ObjectId] = group.current_input_match_id
        if (
            group.mode in (GroupMode.input.value, GroupMode.sim.value, GroupMode.chip_input.value)
            and other_session_match_id is not None
            and other_session_match_id != active_match._id
        ):
            other_match = match_service.find_one_by_id(other_session_match_id)
            other_name = (other_match.name if other_match else None) or "他の対戦"
            reply_service.add_message(
                f"現在「{other_name}」の入力中です。先に完了するか「_exit」で中断してください。",
            )
            return

        hanchans = hanchan_service.find_all_archived_by_match_id(active_match._id)

        if len(hanchans) == 0:
            reply_service.add_message("まだ対戦結果がありません。")
            return

        # 対戦作成時のレート等を使う(グループの現在の設定ではなく)。
        # 異なるレートの対戦が同時に進行していても、それぞれ自分自身の設定で
        # 精算されるようにするため(FEZ-66 Phase D)。settings未設定(旧データ)は
        # グループの現在の設定にフォールバックする。
        settings = active_match.settings or group_setting_service.find_or_create(
            line_group_id,
        )
        chip_rate = settings.chip_rate
        if (
            chip_rate != 0
            and group_service.get_mode(line_group_id) != GroupMode.chip_ok.value
        ):
            # チップ入力セッションの対象として、この対戦を明示的にセッション
            # ポインタへ設定する(他の対戦のセッションを上書きしないことは
            # 上のガードで確認済み)。
            group.current_input_match_id = active_match._id
            group.mode = GroupMode.chip_input.value
            group_service.update(group)
            reply_service.add_chip_complete_button()
            return

        # 精算
        rate = settings.rate * 10
        sum_scores = active_match.sum_scores
        chip_scores = active_match.chip_scores

        sum_prices: Dict[str, int] = {}
        sum_prices_with_chip: Dict[str, int] = {}
        for line_user_id, converted_score in sum_scores.items():
            # チップ設定が有効な場合のみチップを加算
            chip_score = chip_scores.get(line_user_id, 0) if chip_rate != 0 else 0
            # チップを累計ポイントに加算してからレートを掛ける
            total_score = converted_score + chip_score
            price = total_score * rate
            sum_prices[line_user_id] = converted_score * rate
            sum_prices_with_chip[line_user_id] = price

        # 試合のアーカイブ
        active_match.chip_prices = {}
        active_match.sum_prices = sum_prices
        active_match.sum_prices_with_chip = sum_prices_with_chip
        active_match.status = MatchStatus.settled.value
        match_service.update(active_match)

        # このグループの入力セッションが、まさに今精算した対戦を指していた
        # 場合のみクリアする。他の対戦のセッション中にこの対戦を精算しても
        # (ピッカー経由)、そちらのセッション状態には触れない。
        if group.current_input_match_id == active_match._id:
            group.mode = GroupMode.wait.value
            group.current_input_match_id = None
            group_service.update(group)
        logger.info(
            "finish match: group=%s match=%s hanchans=%d",
            line_group_id, active_match._id, len(hanchans),
        )

        # 応答メッセージ作成
        reply_service.add_message(
            "【対戦結果】 \n"
            + message_service.create_show_match_result(match=active_match, unit=settings.unit),
        )

        image_url = CreateMatchDetailGraphUseCase().execute(active_match._id)
        if image_url is not None:
            reply_service.add_image(image_url)
