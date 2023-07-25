from typing import List, Dict, Tuple
from datetime import datetime
from pymongo import ASCENDING
from mongo_client import yakuman_users_collection
from DomainModel.entities.YakumanUser import YakumanUser
from DomainModel.IRepositories.IYakumanUserRepository import IYakumanUserRepository


class YakumanUserRepository(IYakumanUserRepository):

    def create(
        self,
        new_record: YakumanUser,
    ) -> YakumanUser:
        new_dict = new_record.__dict__.copy()
        new_dict['created_at'] = datetime.now()
        new_dict.pop('_id')
        result = yakuman_users_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        new_values['updated_at'] = datetime.now()
        result = yakuman_users_collection.update_many(query, {'$set': new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[YakumanUser]:
        records = yakuman_users_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = yakuman_users_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> YakumanUser:
        domain = YakumanUser()
        for attr, value in record.items():
            domain.__setitem__(attr, value)
        return domain
