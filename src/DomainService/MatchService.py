from typing import List, Optional

from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING

from DomainModel.entities.Match import Match
from repositories import match_repository

from .interfaces.IMatchService import IMatchService

STATUS_LIST = ["disabled", "active", "archived"]


class MatchService(IMatchService):
    def add_or_drop_chip_score(
        self,
        match_id: ObjectId,
        line_user_id: str,
        chip_score: Optional[int],
    ) -> Match:
        if line_user_id is None:
            raise ValueError("fail to add_or_drop_chip_score: line_user_id is required")

        matches = match_repository.find(
            {
                "_id": match_id,
            }
        )

        if len(matches) == 0:
            raise ValueError("Not found match")

        target = matches[0]
        chip_scores = target.chip_scores

        if chip_score is None:
            chip_scores.pop(line_user_id, None)
        else:
            chip_scores[line_user_id] = chip_score

        target.chip_scores = chip_scores
        self.update(target)

        return target

    def find_one_by_id(self, _id: ObjectId) -> Optional[Match]:
        matches = match_repository.find(
            {"_id": _id},
        )
        if len(matches) == 0:
            return None
        return matches[0]

    def create_with_line_group_id(self, line_group_id: str) -> Match:
        new_match = Match(
            line_group_id=line_group_id,
        )
        match_repository.create(new_match)

        print(f'create match: group "{line_group_id}"')
        return new_match

    def update(self, target: Match) -> None:
        match_repository.update(
            {"_id": target._id},
            target.__dict__,
        )

    def find_all_for_graph(self, ids: List[ObjectId]) -> List[Match]:
        # 将来的にはGroupに含まれるメンバーの半荘のみを対象とする
        return match_repository.find(
            query={"_id": {"$in": ids}},
            sort=[("created_at", ASCENDING)],
        )

    def find_all_by_ids_and_line_group_ids(
        self, ids: List[ObjectId], line_group_ids: List[str]
    ) -> List[Match]:
        return match_repository.find(
            query={"_id": {"$in": ids}, "line_group_id": {"$in": line_group_ids}},
        )

    def find_latest_one(self, line_group_id: str) -> Optional[Match]:
        matches = match_repository.find(
            query={"line_group_id": line_group_id},
            sort=[("created_at", DESCENDING)],
        )
        if len(matches) == 0:
            return None
        return matches[0]

    def find_all_archived_by_line_group_id(self, line_group_id: str) -> List[Match]:
        # 将来的にはGroupに含まれるメンバーの半荘のみを対象とする
        return match_repository.find(
            query={
                "line_group_id": line_group_id,
                "sum_prices_with_chip": {"$ne": {}},
            },
            sort=[("created_at", ASCENDING)],
        )
