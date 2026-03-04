import copy
from datetime import datetime
from typing import List, Optional

from domain_model.entities.history_session import HistorySession
from mongo_client import history_sessions_collection


class HistorySessionRepository:

    def create(self, session: HistorySession) -> HistorySession:
        # 既存セッションを上書き（グループごとに1セッション）
        self.delete_by_group_id(session.line_group_id)
        new_dict = {k: v for k, v in session.__dict__.items() if k != "_id"}
        result = history_sessions_collection.insert_one(new_dict)
        session._id = result.inserted_id
        return session

    def find_active_by_group_id(self, line_group_id: str) -> Optional[HistorySession]:
        """expires_at が未来のセッションのみ返す。期限切れまたは未作成は None。"""
        record = history_sessions_collection.find_one(
            {"line_group_id": line_group_id, "expires_at": {"$gt": datetime.now()}}
        )
        if record is None:
            return None
        return self._to_domain(record)

    def update_selected_users(
        self, line_group_id: str, selected_line_ids: List[str]
    ) -> int:
        result = history_sessions_collection.update_one(
            {"line_group_id": line_group_id},
            {"$set": {"selected_line_ids": selected_line_ids}},
        )
        return result.matched_count

    def delete_by_group_id(self, line_group_id: str) -> int:
        result = history_sessions_collection.delete_many(
            {"line_group_id": line_group_id}
        )
        return result.deleted_count

    def _to_domain(self, record: dict) -> HistorySession:
        return HistorySession(
            line_group_id=record.get("line_group_id"),
            requester_line_id=record.get("requester_line_id"),
            selected_line_ids=record.get("selected_line_ids", []),
            expires_at=record.get("expires_at"),
            _id=record.get("_id"),
        )
