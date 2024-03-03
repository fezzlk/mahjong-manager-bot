from typing import List, Dict, Tuple
from pymongo import ASCENDING
from mongo_client import user_hanchans_collection
from DomainModel.entities.UserHanchan import UserHanchan
from DomainModel.IRepositories.IUserHanchanRepository import IUserHanchanRepository


class UserHanchanRepository(IUserHanchanRepository):

    def create(
        self,
        new_record: UserHanchan,
    ) -> UserHanchan:
        if len(self.find(query={
            'line_user_id': new_record.line_user_id,
            'hanchan_id': new_record.hanchan_id,
        })) != 0:
            raise Exception(f'LINE User ID({new_record.line_user_id}とHanchan ID({new_record.hanchan_id}) のUserHanchanはすでに存在しています。')
        new_dict = new_record.__dict__.copy()
        if new_record._id is None:
            new_dict.pop('_id')
        result = user_hanchans_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[UserHanchan]:
        records = user_hanchans_collection\
            .find(filter=query)\
            .sort(sort)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        result = user_hanchans_collection.delete_many(filter=query)
        return result.deleted_count
    
    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        from datetime import datetime
        new_values['updated_at'] = datetime.now()
        result = user_hanchans_collection.update_many(query, {'$set': new_values})
        return result.matched_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> UserHanchan:
        return UserHanchan(
            line_user_id=record.get("line_user_id"),
            hanchan_id=record.get("hanchan_id"),
            point=record.get("point"),
            rank=record.get("rank"),
            yakuman_count=record.get("yakuman_count"),
            created_at=record.get('created_at'),
            updated_at=record.get('updated_at'),
            _id=record.get("_id"),
        )
