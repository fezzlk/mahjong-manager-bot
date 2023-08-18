from typing import List, Dict, Tuple
from datetime import datetime
from pymongo import ASCENDING
from mongo_client import line_users_collection
from DomainModel.entities.User import User
from DomainModel.IRepositories.IUserRepository import IUserRepository


class UserRepository(IUserRepository):

    def create(
        self,
        new_record: User,
    ) -> User:
        if len(self.find(query={'line_user_id': new_record.line_user_id})) != 0:
            raise Exception(f'LINE User ID: {new_record.line_user_id} のUserはすでに存在しています。')

        new_dict = new_record.__dict__.copy()
        if new_record._id is None:
            new_dict.pop('_id')
        result = line_users_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        new_values['updated_at'] = datetime.now()
        result = line_users_collection.update_many(query, {'$set': new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[User]:
        records = line_users_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = line_users_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> User:
        return User(
            line_user_id=record.get("line_user_id"),
            line_user_name=record.get("line_user_name"),
            mode=record.get("mode"),
            jantama_name=record.get("jantama_name"),
            original_id=record.get("original_id"),
            _id=record.get('_id'),
        )
