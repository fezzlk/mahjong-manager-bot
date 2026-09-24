from datetime import datetime
from typing import List, Optional

from domain_model.entities.match_sum_session import MatchSumSession
from mongo_client import match_sum_sessions_collection


class MatchSumSessionRepository:

    # セッションは(グループ, 開始したユーザー)ごとに1つ。同じグループの別メンバーが
    # 並行して選択しても互いの選択を上書き・確定しないようにする。

    def create(self, session: MatchSumSession) -> MatchSumSession:
        # 同じユーザーの既存セッションを上書き
        self.delete(session.line_group_id, session.requester_line_id)
        new_dict = {k: v for k, v in session.__dict__.items() if k != "_id"}
        result = match_sum_sessions_collection.insert_one(new_dict)
        session._id = result.inserted_id
        return session

    def find_active(
        self, line_group_id: str, requester_line_id: str,
    ) -> Optional[MatchSumSession]:
        """expires_at が未来のセッションのみ返す。期限切れまたは未作成は None。"""
        record = match_sum_sessions_collection.find_one(
            {
                "line_group_id": line_group_id,
                "requester_line_id": requester_line_id,
                "expires_at": {"$gt": datetime.now()},
            },
        )
        if record is None:
            return None
        return self._to_domain(record)

    def update_selected_matches(
        self, line_group_id: str, requester_line_id: str, selected_match_ids: List[str],
    ) -> int:
        result = match_sum_sessions_collection.update_one(
            {"line_group_id": line_group_id, "requester_line_id": requester_line_id},
            {"$set": {"selected_match_ids": selected_match_ids}},
        )
        return result.matched_count

    def delete(self, line_group_id: str, requester_line_id: str) -> int:
        result = match_sum_sessions_collection.delete_many(
            {"line_group_id": line_group_id, "requester_line_id": requester_line_id},
        )
        return result.deleted_count

    def _to_domain(self, record: dict) -> MatchSumSession:
        return MatchSumSession(
            line_group_id=record.get("line_group_id"),
            requester_line_id=record.get("requester_line_id"),
            selected_match_ids=record.get("selected_match_ids", []),
            expires_at=record.get("expires_at"),
            _id=record.get("_id"),
        )
