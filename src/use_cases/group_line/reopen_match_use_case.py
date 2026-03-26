from pymongo import DESCENDING

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import GroupMode
from domain_service import (
    group_service,
    match_service,
)
from repositories import match_repository


class ReopenMatchUseCase:
    """清算済みの直前マッチを再アクティブにする。

    レート変更後の再清算を可能にする。
    """

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return

        if group.active_match_id is not None:
            reply_service.add_message(
                "現在進行中の試合があります。先に「_finish」で清算するか「_exit」で中断してください。",
            )
            return

        # 直前の清算済みマッチを取得（最新の is_deleted=False のマッチ）
        matches = match_repository.find(
            {"line_group_id": line_group_id},
            sort=[("_id", DESCENDING)],
            limit=1,
        )

        if len(matches) == 0:
            reply_service.add_message("清算済みの試合が見つかりません。")
            return

        target_match = matches[0]

        # 清算結果をリセット
        target_match.sum_prices = {}
        target_match.chip_prices = {}
        target_match.sum_prices_with_chip = {}
        match_service.update(target_match)

        # グループに再設定
        group.active_match_id = target_match._id
        group.mode = GroupMode.wait.value
        group_service.update(group)

        reply_service.add_message(
            "直前の試合を再オープンしました。\n"
            "レートを変更する場合は「_setting」、再度清算する場合は「_finish」と入力してください。",
        )
