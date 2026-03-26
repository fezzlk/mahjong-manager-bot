"""user_hanchan_service: hanchan.results に embedded された結果を UserHanchan として返す"""

from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from pymongo import ASCENDING

from domain_model.entities.user_hanchan import UserHanchan
from repositories import hanchan_repository

from .interfaces.i_user_hanchan_service import IUserHanchanService


class UserHanchanService(IUserHanchanService):

    def find_all_each_line_user_id(
        self,
        line_user_ids: List[str],
        from_dt: datetime = None,
        to_dt: datetime = None,
    ) -> List[UserHanchan]:
        query_list = [
            {"results": {"$elemMatch": {"line_user_id": {"$in": line_user_ids}}}},
        ]
        if from_dt is not None:
            query_list.append({"created_at": {"$gte": from_dt}})
        if to_dt is not None:
            query_list.append({"created_at": {"$lte": to_dt}})
        hanchans = hanchan_repository.find(
            query={"$and": query_list},
            sort=[("_id", ASCENDING)],
        )
        line_user_ids_set = set(line_user_ids)
        result = []
        for h in hanchans:
            for r in h.results:
                if r.line_user_id in line_user_ids_set:
                    result.append(UserHanchan(
                        line_user_id=r.line_user_id,
                        hanchan_id=h._id,
                        point=r.point,
                        rank=r.rank,
                        yakuman_count=r.yakuman_count,
                        created_at=h.created_at,
                    ))
        return result

    def find_all_with_line_user_ids_and_hanchan_ids(
        self,
        line_user_ids: List[str],
        hanchan_ids: List[ObjectId],
        from_dt: datetime = None,
        to_dt: datetime = None,
    ) -> List[UserHanchan]:
        query_list = [{
            "_id": {"$in": hanchan_ids},
            "results": {"$elemMatch": {"line_user_id": {"$in": line_user_ids}}},
        }]
        if from_dt is not None:
            query_list.append({"created_at": {"$gte": from_dt}})
        if to_dt is not None:
            query_list.append({"created_at": {"$lte": to_dt}})
        hanchans = hanchan_repository.find(
            query={"$and": query_list},
            sort=[("_id", ASCENDING)],
        )
        line_user_ids_set = set(line_user_ids)
        result = []
        for h in hanchans:
            for r in h.results:
                if r.line_user_id in line_user_ids_set:
                    result.append(UserHanchan(
                        line_user_id=r.line_user_id,
                        hanchan_id=h._id,
                        point=r.point,
                        rank=r.rank,
                        yakuman_count=r.yakuman_count,
                        created_at=h.created_at,
                    ))
        return result
