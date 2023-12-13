"""user"""

from .interfaces.IUserMatchService import IUserMatchService
from DomainModel.entities.UserMatch import UserMatch
from repositories import user_match_repository
from typing import List
from bson.objectid import ObjectId
from datetime import datetime


class UserMatchService(IUserMatchService):

    def find_all_by_user_id_list(
            self,
            user_ids: List[ObjectId],
            from_dt: datetime = None, 
            to_dt: datetime = None,
        ) -> List[UserMatch]:
        query_list = [{'user_id': {'$in': user_ids}}]
        if from_dt is not None:
            query_list.append({'created_at': {'$gte': from_dt}})
        if to_dt is not None:
            query_list.append({'created_at': {'$lte': to_dt}})
        return user_match_repository.find(
            query={'$and': query_list},
        )
