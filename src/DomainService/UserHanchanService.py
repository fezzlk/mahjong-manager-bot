"""user"""

from .interfaces.IUserHanchanService import IUserHanchanService
from DomainModel.entities.UserHanchan import UserHanchan
from repositories import user_hanchan_repository
from typing import List
from pymongo import ASCENDING


class UserHanchanService(IUserHanchanService):

    def find_all_each_line_user_id(self, line_user_ids: List[str]) -> List[UserHanchan]:
        return user_hanchan_repository.find(
            {'line_user_id': {'$in': line_user_ids}},
            [('hanchan_id', ASCENDING)]
        )
