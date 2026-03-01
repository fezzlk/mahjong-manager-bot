import copy
from datetime import datetime
from typing import Dict, List, Tuple

from pymongo import ASCENDING

from domain_model.entities.yakuman_user import YakumanUser
from domain_model.i_repositories.i_yakuman_user_repository import (
    IYakumanUserRepository,
)
from mongo_client import yakuman_users_collection


class YakumanUserRepository(IYakumanUserRepository):

    def create(
        self,
        new_record: YakumanUser,
    ) -> YakumanUser:
        new_dict = copy.deepcopy(new_record.__dict__)
        new_dict["created_at"] = datetime.now()
        new_dict.pop("_id")
        result = yakuman_users_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        new_values["updated_at"] = datetime.now()
        result = yakuman_users_collection.update_one(query, {"$set": new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = None,
        sort: List[Tuple[str, any]] = [("_id", ASCENDING)],
        limit: int = 0,
    ) -> List[YakumanUser]:
        records = yakuman_users_collection\
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
        result = yakuman_users_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> YakumanUser:
        domain = YakumanUser()
        for attr, value in record.items():
            domain.__setitem__(attr, value)
        return domain
