from typing import Optional, List
from .interfaces.IMatchService import IMatchService
from repositories import match_repository
from DomainModel.entities.Match import Match
from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING

STATUS_LIST = ['disabled', 'active', 'archived']


class MatchService(IMatchService):

    def add_or_drop_tip_score(
        self,
        match_id: ObjectId,
        line_user_id: str,
        tip_score: Optional[int],
    ) -> Match:
        if line_user_id is None:
            raise ValueError('fail to add_or_drop_tip_score: line_user_id is required')

        matches = match_repository.find({
            '_id': match_id,
        })

        if len(matches) == 0:
            raise ValueError('Not found match')

        target = matches[0]
        tip_scores = target.tip_scores

        if tip_score is None:
            tip_scores.pop(line_user_id, None)
        else:
            tip_scores[line_user_id] = tip_score

        target.tip_scores = tip_scores
        self.update(target)

        return target


    def find_one_by_id(self, _id: ObjectId) -> Optional[Match]:
        matches = match_repository.find(
            {'_id': _id}
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
            {'_id': target._id},
            target.__dict__,
        )

    def find_all_for_graph(self, ids: List[ObjectId]) -> List[Match]:
        # 将来的にはGroupに含まれるメンバーの半荘のみを対象とする
        return match_repository.find(
            query={'_id': {'$in': ids}},
            sort=[('created_at', ASCENDING)]
        )
    
    def find_latest_one(self, line_group_id: str) -> Optional[Match]:
        matches = match_repository.find(
            query={'line_group_id': line_group_id},
            sort=[('created_at', DESCENDING)],
        )
        if len(matches) == 0:
            return None
        return matches[0]

    def find_all_archived_by_line_group_id(self, line_group_id: str) -> List[Match]:
        # 将来的にはGroupに含まれるメンバーの半荘のみを対象とする
        return match_repository.find(
            query={
                'line_group_id': line_group_id,
                'sum_prices_with_tip': {"$ne": {}},
            },
            sort=[('created_at', ASCENDING)]
        )
    