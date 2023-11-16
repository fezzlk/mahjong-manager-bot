"""user"""

from .interfaces.IUserHanchanService import IUserHanchanService
from DomainModel.entities.UserHanchan import UserHanchan
from repositories import user_hanchan_repository
from typing import List
from pymongo import ASCENDING
from datetime import datetime

class UserHanchanService(IUserHanchanService):

    def find_all_each_line_user_id(
            self, 
            line_user_ids: List[str], 
            from_dt: datetime = None, 
            to_dt: datetime = None,
        ) -> List[UserHanchan]:
        query = {'line_user_id': {'$in': line_user_ids}}
        if from_dt is not None:
            query['created_at'] = {'$gte': from_dt}
        if to_dt is not None:
            query['created_at'] = {'$lte': to_dt}
        return user_hanchan_repository.find(
            query,
            [('hanchan_id', ASCENDING)]
        )
