from typing import List, Dict, Tuple
from datetime import datetime
from pymongo import ASCENDING
from mongo_client import group_settings_collection
from DomainModel.entities.GroupSetting import GroupSetting
from DomainModel.IRepositories.IGroupRepository import IGroupSettingRepository


class GroupSettingRepository(IGroupSettingRepository):

    def create(
        self,
        new_record: GroupSetting,
    ) -> GroupSetting:
        new_dict = new_record.__dict__.copy()
        new_dict['created_at'] = datetime.now()
        if new_dict['id'] is None:
            new_dict.pop('id')
        result = group_settings_collection.insert_one(new_dict)
        new_record.id = result.inserted_id
        return new_record

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('id', ASCENDING)],
    ) -> List[GroupSetting]:
        records = group_settings_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_mapping_record_to_domain(record) for record in records]

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
