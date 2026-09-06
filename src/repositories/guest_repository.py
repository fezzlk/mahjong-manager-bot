import copy
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from pymongo import ASCENDING, DESCENDING

from domain_model.entities.guest import Guest
from domain_model.i_repositories.i_guest_repository import IGuestRepository
from mongo_client import guests_collection


class GuestRepository(IGuestRepository):

    def create(
        self,
        new_record: Guest,
    ) -> Guest:
        new_dict = copy.deepcopy(new_record.__dict__)
        if new_record._id is None:
            new_dict.pop("_id")
        result = guests_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        filter_query = {**query, "is_deleted": {"$ne": True}}
        new_values["updated_at"] = datetime.now()
        result = guests_collection.update_one(filter_query, {"$set": new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = None,
        sort: List[Tuple[str, any]] = [("_id", ASCENDING)],
        limit: int = 0,
    ) -> List[Guest]:
        filter_query = {**(query or {}), "is_deleted": {"$ne": True}}
        records = guests_collection.find(filter=filter_query).sort(sort).limit(limit)
        return [self._mapping_record_to_domain(record) for record in records]

    def find_max_guest_number(self, line_group_id: str) -> Optional[int]:
        record = guests_collection.find_one(
            {"line_group_id": line_group_id},
            sort=[("guest_number", DESCENDING)],
        )
        if record is None:
            return None
        return record.get("guest_number")

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> Guest:
        return Guest(
            line_group_id=record.get("line_group_id"),
            guest_number=record.get("guest_number"),
            is_deleted=record.get("is_deleted", False),
            created_at=record.get("created_at"),
            updated_at=record.get("updated_at"),
            _id=record.get("_id"),
        )
