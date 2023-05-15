from typing import List, Dict, Tuple
from datetime import datetime
from pymongo import ASCENDING
from mongo_client import user_groups_collection
from DomainModel.entities.UserGroup import UserGroup
from DomainModel.IRepositories.IUserGroupRepository import IUserGroupRepository


class UserGroupRepository(IUserGroupRepository):

    def create(
        self,
        new_record: UserGroup,
    ) -> UserGroup:
        new_dict = new_record.__dict__.copy()
        new_dict['created_at'] = datetime.now()
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

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> UserGroup:
        return UserGroup(
            line_user_id=record["line_user_id"],
            line_group_id=record["line_group_id"],
            _id=record["_id"],
        )

