from typing import Optional

from bson.errors import InvalidId
from bson.objectid import ObjectId

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.match import Match, MatchStatus
from domain_service import (
    hanchan_service,
    match_service,
)


class DropMatchByIndexUseCase:

    def confirm(self) -> None:
        """_drop_m_confirm?to=<match_id>: 対戦詳細の削除ボタンから、削除の確認を出す。

        対戦詳細を開くたびにボタンが出るため、誤タップで即削除しないよう
        確認を挟む(FEZ-234)。
        """
        target_match = self._find_target()
        if target_match is None:
            return
        reply_service.add_drop_match_confirm_quick_reply(target_match)

    def select(self) -> None:
        """_drop_m_select?to=<match_id>: 確認後、指定された対戦を削除する。"""
        target_match = self._find_target()
        if target_match is None:
            return

        hanchan_service.disable_by_match_id(match_id=target_match._id)
        target_match.is_deleted = True
        match_service.update(target_match)
        reply_service.add_message(
            f"「{target_match.name or target_match._id}」の対戦結果を削除しました。",
        )

    def _find_target(self) -> Optional[Match]:
        """paramsのtoが指す対戦を、このグループの精算済み対戦であるか再検証して返す。"""
        line_group_id = request_info_service.req_line_group_id
        match_id = request_info_service.params.get("to")

        if not match_id:
            reply_service.add_message("削除する対戦が指定されていません。")
            return None

        try:
            target_match = match_service.find_one_by_id(ObjectId(match_id))
        except InvalidId:
            target_match = None
        if (
            target_match is None
            or target_match.line_group_id != line_group_id
            or target_match.status != MatchStatus.settled.value
        ):
            reply_service.add_message("指定された対戦が見つかりません。")
            return None
        return target_match

    def execute(self, str_index: str) -> None:
        line_group_id = request_info_service.req_line_group_id
        archived_matches = match_service.find_all_archived_by_line_group_id(line_group_id=line_group_id)
        if not str_index.isdigit():
            reply_service.add_message(
                "引数は整数で指定してください。",
            )
            return

        index = int(str_index)
        if index < 1 or len(archived_matches) < index:
            reply_service.add_message(
                f"このトークルームには全{len(archived_matches)}回までしか登録されていないため第{index}回はありません。",
            )
            return

        target_match = archived_matches[index-1]
        hanchan_service.disable_by_match_id(match_id=target_match._id)
        target_match.is_deleted = True
        match_service.update(target_match)
        reply_service.add_message(
            f"第{index}回の対戦結果を削除しました。",
        )
