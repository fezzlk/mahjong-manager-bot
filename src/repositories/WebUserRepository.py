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
        if len(self.find(query={'user_code': new_record.user_code})) != 0:
            raise Exception(f'User Code: {new_record.user_code} のWeb Userはすでに存在しています。')

        new_dict = new_record.__dict__.copy()
        if new_record._id is None:
            new_dict.pop('_id')
        result = web_users_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        new_values['updated_at'] = datetime.now()
        result = web_users_collection.update_many(query, {'$set': new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[WebUser]:
        records = web_users_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = web_users_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> WebUser:
        return WebUser(
            _id=record.get("_id"),
            user_code=record.get("user_code"),
            name=record.get("name"),
            email=record.get("email"),
            linked_line_user_id=record.get("linked_line_user_id"),
            is_approved_line_user=record.get("is_approved_line_user"),
            created_at=record.get("created_at"),
            updated_at=record.get("updated_at"),
        )
