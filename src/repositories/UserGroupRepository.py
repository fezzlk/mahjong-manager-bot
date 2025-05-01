from typing import List, Dict, Tuple
from pymongo import ASCENDING
from mongo_client import user_groups_collection
from DomainModel.entities.UserGroup import UserGroup
from DomainModel.IRepositories.IUserGroupRepository import IUserGroupRepository


class UserGroupRepository(IUserGroupRepository):

    def create(
        self,
        new_record: UserGroup,
    ) -> UserGroup:
        if len(self.find(query={
            'line_user_id': new_record.line_user_id,
            'line_group_id': new_record.line_group_id,
        })) != 0:
            raise Exception(f'LINE User ID({new_record.line_user_id}とLINE Group ID({new_record.line_group_id}) のUserGroupはすでに存在しています。')

        new_dict = new_record.__dict__.copy()
        if new_record._id is None:
            new_dict.pop('_id')
        result = user_groups_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[UserGroup]:
        records = user_groups_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = user_groups_collection.delete_many(filter=query)
        return result.deleted_count

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        from datetime import datetime
        new_values['updated_at'] = datetime.now()
        result = user_groups_collection.update_many(query, {'$set': new_values})
        return result.matched_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> UserGroup:
        return UserGroup(
            line_user_id=record.get("line_user_id"),
            line_group_id=record.get("line_group_id"),
            created_at=record.get('created_at'),
            updated_at=record.get('updated_at'),
            _id=record.get("_id"),
        )
