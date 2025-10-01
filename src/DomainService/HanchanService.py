from typing import List, Optional

from bson.objectid import ObjectId
from pymongo import ASCENDING

from DomainModel.entities.Hanchan import Hanchan
from repositories import hanchan_repository

from .interfaces.IHanchanService import IHanchanService

STATUS_LIST = ["disabled", "active", "archived"]


class HanchanService(IHanchanService):

    def add_or_drop_raw_score(
        self,
        hanchan_id: ObjectId,
        line_user_id: str,
        raw_score: Optional[int],
    ) -> Hanchan:
        if line_user_id is None:
            raise ValueError("fail to add_or_drop_raw_score: line_user_id is required")

        target = self.find_one_by_id(hanchan_id)

        if target is None:
            raise ValueError("fail to add_or_drop_raw_score: Not found hanchan")

        raw_scores = target.raw_scores

        if raw_score is None:
            raw_scores.pop(line_user_id, None)
        else:
            raw_scores[line_user_id] = raw_score

        hanchan_repository.update(
            {"_id": target._id},
            {"raw_scores": raw_scores},
        )

        target.raw_scores = raw_scores
        return target

    def find_one_by_id(self, _id: ObjectId) -> Optional[Hanchan]:
        matches = hanchan_repository.find(
            {"_id": _id},
        )
        if len(matches) == 0:
            return None
        return matches[0]

    def create_with_line_group_id_and_match_id(self, line_group_id: str, match_id: ObjectId) -> Hanchan:
        new_match = Hanchan(
            line_group_id=line_group_id,
            match_id=match_id,
        )
        hanchan_repository.create(new_match)

        print(f'create hanchan: group "{line_group_id}"')
        return new_match

    def find_all_archived_by_match_id(self, match_id: ObjectId) -> List[Hanchan]:
        return hanchan_repository.find(
            {
                "match_id": match_id,
                "converted_scores": {"$ne": {}},
            },
            [("_id", ASCENDING)],
        )

    def find_all_archived_by_match_ids(self, match_ids: List[ObjectId]) -> List[Hanchan]:
        return hanchan_repository.find(
            {
                "match_id": {"$in": match_ids},
                "converted_scores": {"$ne": {}},
            },
            [("_id", ASCENDING)],
        )

    def update(self, target: Hanchan) -> None:
        hanchan_repository.update(
            {"_id": target._id},
            target.__dict__,
        )

    def disable_by_match_id(self, match_id: ObjectId) -> None:
        hanchan_repository.update(
            {"match_id": match_id},
            {"status": 0},
        )
