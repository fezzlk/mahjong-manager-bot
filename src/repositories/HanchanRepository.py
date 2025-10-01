from datetime import datetime
from typing import Dict, List, Tuple

from pymongo import ASCENDING

from DomainModel.entities.Hanchan import Hanchan
from DomainModel.IRepositories.IHanchanRepository import IHanchanRepository
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
        new_values["updated_at"] = datetime.now()
        query["status"] = 2
        result = hanchans_collection.update_many(query, {"$set": new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [("_id", ASCENDING)],
    ) -> List[Hanchan]:
        query["status"] = 2
        records = hanchans_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = hanchans_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> Hanchan:
        return Hanchan(
            line_group_id=record.get("line_group_id"),
            match_id=record.get("match_id"),
            status=record.get("status"),
            raw_scores=record.get("raw_scores"),
            converted_scores=record.get("converted_scores"),
            created_at=record.get("created_at"),
            updated_at=record.get("updated_at"),
            _id=record.get("_id"),
        )
