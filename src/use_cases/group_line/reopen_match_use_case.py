from bson.errors import InvalidId
from bson.objectid import ObjectId
from pymongo import DESCENDING

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import GroupMode
from domain_model.entities.match import MatchStatus
from domain_service import (
    group_service,
    match_service,
)
from repositories import match_repository


class ReopenMatchUseCase:
    """清算済みの対戦を選び直して再アクティブにする。

    レート変更後の再清算を可能にする。
    """

    def execute(self) -> None:
        """_reopen: 直近5件の精算済み対戦から選択する Quick Reply を表示する。"""
        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return

        if group.active_match_id is not None or group.mode == GroupMode.sim.value:
            reply_service.add_message(
                "現在進行中の試合があります。先に「_finish」で清算するか「_exit」で中断してください。",
            )
            return

        matches = match_repository.find(
            {"line_group_id": line_group_id, "status": MatchStatus.settled.value},
            sort=[("_id", DESCENDING)],
            limit=5,
        )

        if len(matches) == 0:
            reply_service.add_message("清算済みの試合が見つかりません。")
            return

        reply_service.add_reopen_target_quick_reply(matches)

    def confirm(self) -> None:
        """_reopen_confirm?to=<match_id>: 再オープンを確定する。"""
        line_group_id = request_info_service.req_line_group_id
        match_id = request_info_service.params.get("to")
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return

        if group.active_match_id is not None or group.mode == GroupMode.sim.value:
            reply_service.add_message(
                "現在進行中の試合があります。先に「_finish」で清算するか「_exit」で中断してください。",
            )
            return

        if not match_id:
            reply_service.add_message("再オープンする対戦が指定されていません。")
            return

        try:
            target_match = match_service.find_one_by_id(ObjectId(match_id))
        except InvalidId:
            target_match = None
        if target_match is None or target_match.line_group_id != line_group_id:
            reply_service.add_message("指定された対戦が見つかりません。")
            return

        # 清算結果をリセット
        target_match.sum_prices = {}
        target_match.chip_prices = {}
        target_match.sum_prices_with_chip = {}
        target_match.status = MatchStatus.open.value
        match_service.update(target_match)

        # グループに再設定
        group.active_match_id = target_match._id
        group.mode = GroupMode.wait.value
        group_service.update(group)

        reply_service.add_message(
            f"「{target_match.name or target_match._id}」を再オープンしました。\n"
            "レートを変更する場合は「_setting」、再度清算する場合は「_finish」と入力してください。",
        )
