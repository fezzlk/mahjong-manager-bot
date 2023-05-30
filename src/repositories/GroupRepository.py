from typing import List, Dict, Tuple
from datetime import datetime
from pymongo import ASCENDING
from mongo_client import groups_collection
from DomainModel.entities.Group import Group
from DomainModel.IRepositories.IGroupRepository import IGroupRepository


class GroupRepository(IGroupRepository):

    def create(
        self,
        new_record: Group,
    ) -> Group:
        if len(self.find(query={'line_group_id': new_record.line_group_id})) != 0:
            raise Exception(f'LINE Group ID: {new_record.line_group_id} のGroupはすでに存在しています。')

        new_dict = new_record.__dict__.copy()
        new_dict['created_at'] = datetime.now()
        new_dict.pop('_id')
        result = groups_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        new_values['updated_at'] = datetime.now()
        result = groups_collection.update_one(query, {'$set': new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[Group]:
        records = groups_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = groups_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> Group:
        return Group(
            line_group_id=record['line_group_id'],
            mode=record['mode'],
            _id=record['_id'],
        )
