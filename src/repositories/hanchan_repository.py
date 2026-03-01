from datetime import datetime
from typing import Dict, List, Tuple

from pymongo import ASCENDING

from domain_model.entities.hanchan import Hanchan
from domain_model.i_repositories.i_hanchan_repository import IHanchanRepository
from mongo_client import hanchans_collection


class HanchanRepository(IHanchanRepository):

    def create(
        self,
        new_record: Hanchan,
    ) -> Hanchan:
        new_dict = new_record.__dict__.copy()
        if new_record._id is None:
            new_dict.pop("_id")
        result = hanchans_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        filter_query = {**query, "is_deleted": {"$ne": True}}
        new_values["updated_at"] = datetime.now()
        result = hanchans_collection.update_many(filter_query, {"$set": new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = None,
        sort: List[Tuple[str, any]] = [("_id", ASCENDING)],
        limit: int = 0,
    ) -> List[Hanchan]:
        filter_query = {**(query or {}), "is_deleted": {"$ne": True}}
        records = hanchans_collection\
            .find(filter=filter_query)\
            .sort(sort)\
            .limit(limit)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = None,
    ) -> int:
        if not query:
            raise ValueError("delete() requires a non-empty query to prevent accidental full-collection deletion")
        result = hanchans_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> Hanchan:
        return Hanchan(
            line_group_id=record.get("line_group_id"),
            match_id=record.get("match_id"),
            is_deleted=record.get("is_deleted", False),
            raw_scores=record.get("raw_scores"),
            converted_scores=record.get("converted_scores"),
            created_at=record.get("created_at"),
            updated_at=record.get("updated_at"),
            _id=record.get("_id"),
        )
