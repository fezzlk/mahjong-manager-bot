from typing import List, Optional

from bson.errors import InvalidId
from bson.objectid import ObjectId

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import GroupMode
from domain_model.entities.match import MatchStatus
from domain_service import (
    group_service,
    hanchan_service,
    match_service,
    user_service,
)


class DropHanchanByIndexUseCase:
    def execute(self, str_index: str) -> None:
        if not str_index.isdigit():
            reply_service.add_message(
                "引数は整数で指定してください。",
            )
            return
        index = int(str_index)

        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "トークルームが登録されていません。招待し直してください。",
            )
            return
        if group.current_input_match_id is None:
            reply_service.add_message(
                "現在進行中の対戦がありません。",
            )
            return

        active_match = match_service.find_one_by_id(group.current_input_match_id)
        if active_match is None:
            raise RuntimeError(
                f"DropHanchanByIndexUseCase: 対戦結果の取得失敗: match_id: {group.current_input_match_id}",
            )

        archived_hanchans = hanchan_service.find_all_archived_by_match_id(
            match_id=active_match._id,
        )

        if index < 1 or len(archived_hanchans) < index:
            reply_service.add_message(
                f"このトークルームには全{len(archived_hanchans)}回までしか登録されていないため第{index}回はありません。",
            )
            return

        target_hanchan = archived_hanchans[index - 1]
        target_hanchan.is_deleted = True
        hanchan_service.update(target_hanchan)
        self._reply_dropped(index, target_hanchan, active_match)

    def select(self) -> None:
        """_drop_select?to=<hanchan_id>: ボタン選択で指定された半荘を削除する。"""
        line_group_id = request_info_service.req_line_group_id
        hanchan_id = request_info_service.params.get("to")

        if not hanchan_id:
            reply_service.add_message("削除する半荘が指定されていません。")
            return

        try:
            target_hanchan = hanchan_service.find_one_by_id(ObjectId(hanchan_id))
        except InvalidId:
            target_hanchan = None
        if target_hanchan is None or target_hanchan.is_deleted:
            reply_service.add_message("指定された半荘が見つかりません。")
            return

        # ボタンが表示されていた時点から対戦の状態が変わっていないか
        # (紐づくMatchがこのグループのopenな対戦であるか)を再検証する
        target_match = match_service.find_one_by_id(target_hanchan.match_id)
        if (
            target_match is None
            or target_match.line_group_id != line_group_id
            or target_match.status != MatchStatus.open.value
        ):
            reply_service.add_message("指定された半荘が見つかりません。")
            return

        archived_hanchans = hanchan_service.find_all_archived_by_match_id(
            match_id=target_match._id,
        )
        index = next(
            (i + 1 for i, h in enumerate(archived_hanchans) if h._id == target_hanchan._id),
            None,
        )
        if index is None:
            reply_service.add_message("指定された半荘が見つかりません。")
            return

        target_hanchan.is_deleted = True
        hanchan_service.update(target_hanchan)
        self._reply_dropped(index, target_hanchan, target_match)

    def _reply_dropped(self, index: int, hanchan, match) -> None:
        """削除完了を伝え、素点一覧を貼り付け登録できる形式で添える。

        AddHanchanByPointsTextUseCase.parse_replyが受け付ける「名前: 点数」形式
        (点数入力時のBotの返信と同じ)で出すため、コピペで再登録できる。
        ただし、貼り付けても元の対戦に正しく再登録できる場合に限る。
        """
        reply_service.add_message(
            f"現在の対戦の第{index}半荘の結果を削除しました。",
        )
        if not self._paste_would_target(match):
            return
        rows = self._pasteable_rows(hanchan.raw_scores or {})
        if rows is None:
            return
        reply_service.add_message(
            "入力し直す場合は、次のメッセージをそのままコピーして貼り付けると再登録できます。",
        )
        reply_service.add_message("\n".join(rows))

    @staticmethod
    def _paste_would_target(match) -> bool:
        """素点一覧の貼り付け登録(AddHanchanByPointsTextUseCase)が、この対戦を登録先に選ぶか。

        貼り付け登録は入力中の対戦(current_input_match_id)、それが無ければ
        唯一のopen対戦を登録先にする。別の対戦に入ってしまう状況では案内しない。
        """
        group = group_service.find_one_by_line_group_id(match.line_group_id)
        if group is None or group.mode not in (GroupMode.wait.value, GroupMode.input.value):
            return False
        if group.current_input_match_id is not None:
            return group.current_input_match_id == match._id
        open_matches = match_service.find_all_open_by_line_group_id(match.line_group_id)
        return len(open_matches) == 1 and open_matches[0]._id == match._id

    @staticmethod
    def _pasteable_rows(raw_scores) -> Optional[List[str]]:
        """各名前が貼り付け時に元の本人へ一意に戻る場合だけ「名前: 点数」の行を返す。"""
        if len(raw_scores) < 2:
            return None
        rows = []
        for line_user_id, raw_score in raw_scores.items():
            name = user_service.get_name_by_line_user_id(line_user_id)
            if (
                name is None
                or name == "友達未登録"
                or user_service.get_line_user_id_by_name(name) != line_user_id
            ):
                return None
            rows.append(f"{name}: {raw_score}")
        return rows
