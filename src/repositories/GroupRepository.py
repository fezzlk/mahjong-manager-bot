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
        new_dict = new_record.__dict__.copy()
        new_dict['created_at'] = datetime.now()
        if new_dict['id'] is None:
            new_dict.pop('id')
        result = groups_collection.insert_one(new_dict)
        new_record.id = result.inserted_id
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
        sort: List[Tuple[str, any]] = [('id', ASCENDING)],
    ) -> List[Group]:
        records = groups_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = groups_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> Group:
        domain = Group()
        for attr, value in record.items():
            domain.__setitem__(attr, value)
        return domain
