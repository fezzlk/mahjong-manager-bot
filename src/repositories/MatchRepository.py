from datetime import datetime
from typing import Dict, List, Tuple

from pymongo import ASCENDING

from DomainModel.entities.Match import Match
from DomainModel.IRepositories.IMatchRepository import IMatchRepository
from mongo_client import matches_collection


class MatchRepository(IMatchRepository):
    def create(
        self,
        new_record: Match,
    ) -> Match:
        new_dict = new_record.__dict__.copy()
        if new_record._id is None:
            new_dict.pop("_id")
        result = matches_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        query["status"] = 2
        new_values["updated_at"] = datetime.now()
        result = matches_collection.update_many(query, {"$set": new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [("_id", ASCENDING)],
    ) -> List[Match]:
        query["status"] = 2
        records = matches_collection.find(filter=query).sort(sort)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = matches_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> Match:
        return Match(
            line_group_id=record.get("line_group_id"),
            status=record.get("status"),
            created_at=record.get("created_at"),
            updated_at=record.get("updated_at"),
            chip_scores=record.get("chip_scores", {}),
            chip_prices=record.get("chip_prices", {}),
            active_hanchan_id=record.get("active_hanchan_id"),
            sum_scores=record.get("sum_scores", {}),
            sum_prices=record.get("sum_prices", {}),
            sum_prices_with_chip=record.get("sum_prices_with_chip", {}),
            _id=record.get("_id"),
            original_id=record.get("original_id"),
        )
