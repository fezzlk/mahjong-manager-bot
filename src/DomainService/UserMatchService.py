"""user"""

from .interfaces.IUserMatchService import IUserMatchService
from DomainModel.entities.UserMatch import UserMatch
from repositories import user_match_repository
from typing import List
from bson.objectid import ObjectId


class UserMatchService(IUserMatchService):

    def find_all_by_user_id_list(self, user_ids: List[ObjectId]) -> List[UserMatch]:
        return user_match_repository.find(
            {'user_id': {'$in': user_ids}},
        )
