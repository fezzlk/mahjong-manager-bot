from typing import List, Dict, Tuple
from datetime import datetime
from pymongo import ASCENDING
from mongo_client import hanchan_matches_collection
from DomainModel.entities.HanchanMatch import HanchanMatch
from DomainModel.IRepositories.IHanchanMatchRepository import IHanchanMatchRepository


class HanchanMatchRepository(IHanchanMatchRepository):

    def create(
        self,
        new_record: HanchanMatch,
    ) -> HanchanMatch:
        new_dict = new_record.__dict__.copy()
        new_dict['created_at'] = datetime.now()
        new_dict.pop('_id')
        result = hanchan_matches_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[HanchanMatch]:
        records = hanchan_matches_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = hanchan_matches_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> HanchanMatch:
        return HanchanMatch(
            hanchan_id=record["hanchan_id"],
            match_id=record["match_id"],
            _id=record["_id"],
        )
