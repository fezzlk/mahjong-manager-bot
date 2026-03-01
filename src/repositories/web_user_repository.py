from datetime import datetime
from typing import Dict, List, Tuple

from pymongo import ASCENDING

from domain_model.entities.web_user import WebUser
from domain_model.i_repositories.i_web_user_repository import IWebUserRepository
from mongo_client import web_users_collection


class WebUserRepository(IWebUserRepository):

    def create(
        self,
        new_record: WebUser,
    ) -> WebUser:
        if len(self.find(query={"user_code": new_record.user_code})) != 0:
            raise Exception(f"User Code: {new_record.user_code} のWeb Userはすでに存在しています。")

        new_dict = new_record.__dict__.copy()
        if new_record._id is None:
            new_dict.pop("_id")
        result = web_users_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        new_values["updated_at"] = datetime.now()
        result = web_users_collection.update_one(query, {"$set": new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = None,
        sort: List[Tuple[str, any]] = [("_id", ASCENDING)],
        limit: int = 0,
    ) -> List[WebUser]:
        records = web_users_collection\
            .find(filter=dict(query) if query is not None else {})\
            .sort(sort)\
            .limit(limit)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = None,
    ) -> int:
        if not query:
            raise ValueError("delete() requires a non-empty query to prevent accidental full-collection deletion")
        result = web_users_collection.delete_many(filter=query)
        return result.deleted_count

    def find_by_id(self, _id) -> WebUser:
        records = self.find(query={"_id": _id})
        return records[0] if len(records) > 0 else None

    def update_linked_line_user_id(
        self,
        _id,
        line_user_id: str,
    ) -> int:
        return self.update(
            query={"_id": _id},
            new_values={"linked_line_user_id": line_user_id},
        )

    def reset_line(self, _id) -> int:
        return self.update(
            query={"_id": _id},
            new_values={
                "linked_line_user_id": "",
                "is_approved_line_user": False,
            },
        )

    def approve_line(self, _id) -> int:
        return self.update(
            query={"_id": _id},
            new_values={
                "is_approved_line_user": True,
            },
        )

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> WebUser:
        return WebUser(
            _id=record.get("_id"),
            user_code=record.get("user_code"),
            name=record.get("name"),
            email=record.get("email"),
            linked_line_user_id=record.get("linked_line_user_id"),
            is_approved_line_user=record.get("is_approved_line_user"),
            created_at=record.get("created_at"),
            updated_at=record.get("updated_at"),
        )
