from typing import List, Dict, Tuple
from datetime import datetime
from pymongo import ASCENDING
from mongo_client import user_matches_collection
from DomainModel.entities.UserMatch import UserMatch
from DomainModel.IRepositories.IUserMatchRepository import IUserMatchRepository


class UserMatchRepository(IUserMatchRepository):

    def create(
        self,
        new_record: UserMatch,
    ) -> UserMatch:
        new_dict = new_record.__dict__.copy()
        new_dict['created_at'] = datetime.now()
        new_dict.pop('_id')
        result = user_matches_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[UserMatch]:
        records = user_matches_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = user_matches_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> UserMatch:
        domain = UserMatch()
        for attr, value in record.items():
            domain.__setitem__(attr, value)
        return domain
