from typing import List, Dict, Tuple
from datetime import datetime
from pymongo import ASCENDING
from mongo_client import web_users_collection
from DomainModel.entities.WebUser import WebUser
from DomainModel.IRepositories.IWebUserRepository import IWebUserRepository


class WebUserRepository(IWebUserRepository):

    def create(
        self,
        new_record: WebUser,
    ) -> WebUser:
        new_dict = new_record.__dict__.copy()
        new_dict['created_at'] = datetime.now()
        if new_dict['id'] is None:
            new_dict.pop('id')
        result = web_users_collection.insert_one(new_dict)
        new_record.id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        new_values['updated_at'] = datetime.now()
        result = web_users_collection.update_one(query, {'$set': new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('id', ASCENDING)],
    ) -> List[WebUser]:
        records = web_users_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = web_users_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> WebUser:
        domain = WebUser()
        for attr, value in record.items():
            domain.__setitem__(attr, value)
        return domain
