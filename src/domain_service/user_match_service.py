"""user"""

from datetime import datetime
from typing import List

from bson.objectid import ObjectId

from domain_model.entities.user_match import UserMatch
from repositories import user_match_repository

from .interfaces.i_user_match_service import IUserMatchService


class UserMatchService(IUserMatchService):

    def find_all_by_user_id_list(
        self,
        user_ids: List[ObjectId],
        from_dt: datetime = None,
        to_dt: datetime = None,
    ) -> List[UserMatch]:
        query_list = [{"user_id": {"$in": user_ids}}]
        if from_dt is not None:
            query_list.append({"created_at": {"$gte": from_dt}})
        if to_dt is not None:
            query_list.append({"created_at": {"$lte": to_dt}})
        return user_match_repository.find(
            query={"$and": query_list},
        )
