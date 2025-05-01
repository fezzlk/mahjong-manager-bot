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
        if len(self.find(query={'line_group_id': new_record.line_group_id})) != 0:
            raise Exception(f'LINE Group ID: {new_record.line_group_id} のGroupSettingはすでに存在しています。')

        new_dict = new_record.__dict__.copy()
        if new_record._id is None:
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
        result = group_settings_collection.update_many(query, {'$set': new_values})
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
        return GroupSetting(
            _id=record.get("_id"),
            line_group_id=record.get("line_group_id"),
            rate=record.get("rate"),
            ranking_prize=record.get("ranking_prize"),
            tobi_prize=record.get("tobi_prize"),
            tip_rate=record.get("tip_rate"),
            num_of_players=record.get("num_of_players"),
            rounding_method=record.get("rounding_method"),
            created_at=record.get('created_at'),
            updated_at=record.get('updated_at'),
        )
