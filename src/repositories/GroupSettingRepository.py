from typing import List, Dict, Tuple
from datetime import datetime
from pymongo import ASCENDING
from mongo_client import group_settings_collection
from DomainModel.entities.GroupSetting import GroupSetting
from DomainModel.IRepositories.IGroupSettingRepository import IGroupSettingRepository


class GroupSettingRepository(IGroupSettingRepository):

    def create(
        self,
        new_record: GroupSetting,
    ) -> GroupSetting:
        new_dict = new_record.__dict__.copy()
        new_dict['created_at'] = datetime.now()
        new_dict.pop('_id')
        result = group_settings_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        new_values['updated_at'] = datetime.now()
        result = group_settings_collection.update_one(query, {'$set': new_values})
        return result.matched_count
    
    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[GroupSetting]:
        records = group_settings_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = group_settings_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> GroupSetting:
        domain = GroupSetting()
        for attr, value in record.items():
            domain.__setitem__(attr, value)
        return domain
