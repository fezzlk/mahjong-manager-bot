from typing import Optional

from bson.errors import InvalidId
from bson.objectid import ObjectId

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import GroupMode
from domain_model.entities.match import Match, MatchStatus
from domain_service import (
    group_service,
    group_setting_service,
    match_service,
    user_service,
)


class ReplyApplyBadaiUseCase:
    def execute(self, badai: str) -> None:
        """_badai <金額>: 直前の対戦に場代を適用した最終会計を表示する(手打ち、後方互換)。"""
        amount = self._parse(badai)
        if amount is None:
            return

        line_group_id = request_info_service.req_line_group_id

        latest_match = match_service.find_latest_one(line_group_id=line_group_id)

        if latest_match is None:
            reply_service.add_message("まだ対戦結果がありません。")
            return

        if (
            latest_match.sum_prices_with_chip is None
            or len(latest_match.sum_prices_with_chip) == 0
        ):
            reply_service.add_message(
                "現在進行中の対戦があります。対戦を終了するには「_finish」と送信してください。",
            )
            return

        reply_service.add_message("直前の対戦の最終会計を表示します。")
        self._show(line_group_id, latest_match, amount)

    def start(self) -> None:
        """_badai_start?to=<match_id>: 精算結果の「場代を入力」ボタンから場代入力モードに入る。"""
        line_group_id = request_info_service.req_line_group_id
        match_id = request_info_service.params.get("to")
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return

        target_match = self._find_settled_match(line_group_id, match_id)
        if target_match is None:
            reply_service.add_message("指定された対戦が見つかりません。")
            return

        # group.modeはグループ全体で1つしか持てないため、他の入力中は開始しない
        if group.mode not in (GroupMode.wait.value, GroupMode.badai_input.value):
            reply_service.add_message(
                "現在、別の入力が進行中のため場代を入力できません。入力が完了してから実行してください。",
            )
            return

        group.mode = GroupMode.badai_input.value
        group.current_input_match_id = target_match._id
        group_service.update(group)
        reply_service.add_message_with_exit_button(
            "場代の合計金額を数字で送ってください。(例: 5000)",
        )

    def input(self, text: str) -> None:
        """badai_inputモード中に送られた金額で、対象の対戦の最終会計を表示する。"""
        amount = self._parse(text)
        if amount is None:
            # 入力し直せるようモードは維持する
            return

        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return

        target_match = match_service.find_one_by_id(group.current_input_match_id)

        group.mode = GroupMode.wait.value
        group.current_input_match_id = None
        group_service.update(group)

        if (
            target_match is None
            or target_match.line_group_id != line_group_id
            or target_match.status != MatchStatus.settled.value
        ):
            # 入力待ちの間に再オープン・削除された場合など
            reply_service.add_message("対象の対戦が見つかりません。精算からやり直してください。")
            return

        reply_service.add_message("場代込みの最終会計を表示します。")
        self._show(line_group_id, target_match, amount)

    def _parse(self, text: str) -> Optional[int]:
        text = text.strip().replace(",", "")
        if not text.isdigit():
            reply_service.add_message(
                "場代は自然数で入力してください。",
            )
            return None
        return int(text)

    def _find_settled_match(self, line_group_id: str, match_id) -> Optional[Match]:
        if not match_id:
            return None
        try:
            match = match_service.find_one_by_id(ObjectId(match_id))
        except InvalidId:
            return None
        if (
            match is None
            or match.line_group_id != line_group_id
            or match.status != MatchStatus.settled.value
        ):
            return None
        return match

    def _show(self, line_group_id: str, match: Match, badai: int) -> None:
        player_count = len(match.sum_prices_with_chip)

        setting = group_setting_service.find_or_create(line_group_id)
        unit = setting.unit

        badai_per_player = badai // player_count
        fraction = badai % player_count
        if fraction != 0:
            badai_per_player += 1
            fraction -= player_count
        str_fraction = "" if fraction == 0 else str(fraction) + unit

        str_each_price = []
        for u_id, p in match.sum_prices_with_chip.items():
            name = user_service.get_name_by_line_user_id(u_id) or "友達未登録"
            str_each_price.append(f"{name}: {p - badai_per_player}{unit}")

        reply_service.add_message(
            "対戦開始日: "
            + match.created_at.strftime("%Y年%m月%d日")
            + "\n"
            + f"場代: {badai}{unit}({badai_per_player}{unit}×{player_count}人{str_fraction})"
            + "\n"
            + "\n".join(str_each_price),
        )
