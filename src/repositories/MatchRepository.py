from typing import List, Dict, Tuple
from datetime import datetime
from pymongo import ASCENDING
from mongo_client import matches_collection
from DomainModel.entities.Match import Match
from DomainModel.IRepositories.IMatchRepository import IMatchRepository


class MatchRepository(IMatchRepository):

    def create(
        self,
        new_record: Match,
    ) -> Match:
        new_dict = new_record.__dict__.copy()
        new_dict['created_at'] = datetime.now()
        if new_dict['id'] is None:
            new_dict.pop('id')
        result = matches_collection.insert_one(new_dict)
        new_record.id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        new_values['updated_at'] = datetime.now()
        result = matches_collection.update_one(query, {'$set': new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('id', ASCENDING)],
    ) -> List[Match]:
        records = matches_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = matches_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> Match:
        domain = Match()
        for attr, value in record.items():
            domain.__setitem__(attr, value)
        return domain
