"""user"""

from .interfaces.IUserHanchanService import IUserHanchanService
from DomainModel.entities.UserHanchan import UserHanchan
from repositories import user_hanchan_repository
from typing import List
from pymongo import ASCENDING
from datetime import datetime
from bson.objectid import ObjectId


class UserHanchanService(IUserHanchanService):

    def find_all_each_line_user_id(
        self,
        line_user_ids: List[str],
        from_dt: datetime = None,
        to_dt: datetime = None,
    ) -> List[UserHanchan]:
        query_list = [{'line_user_id': {'$in': line_user_ids}}]
        if from_dt is not None:
            query_list.append({'created_at': {'$gte': from_dt}})
        if to_dt is not None:
            query_list.append({'created_at': {'$lte': to_dt}})
        return user_hanchan_repository.find(
            query={'$and': query_list},
            sort=[('hanchan_id', ASCENDING)]
        )

    def find_all_with_line_user_ids_and_hanchan_ids(
        self,
        line_user_ids: List[str],
        hanchan_ids: List[ObjectId],
        from_dt: datetime = None,
        to_dt: datetime = None,
    ) -> List[UserHanchan]:
        query_list = [{
            'hanchan_id': {'$in': hanchan_ids},
            'line_user_id': {'$in': line_user_ids},
        }]
        if from_dt is not None:
            query_list.append({'created_at': {'$gte': from_dt}})
        if to_dt is not None:
            query_list.append({'created_at': {'$lte': to_dt}})
        return user_hanchan_repository.find(
            query={'$and': query_list},
            sort=[('hanchan_id', ASCENDING)]
        )
