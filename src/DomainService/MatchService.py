from typing import Optional
from .interfaces.IMatchService import IMatchService
from repositories import match_repository
from DomainModel.entities.Match import Match

STATUS_LIST = ['disabled', 'active', 'archived']


class MatchService(IMatchService):

    def find_or_create_current(self, line_group_id: str) -> Match:
        current = self.get_current(line_group_id)

        if current is None:
            new_match = Match(
                line_group_id=line_group_id,
                status=1,
            )
            match_repository.create(new_match)

            print(f'create match: group "{line_group_id}"')
            current = new_match

        return current

    def get_current(self, line_group_id: str) -> Match:
        matches = match_repository.find(
            {'$and': [
                {'line_group_id': line_group_id},
                {'status': 1},
            ]})
        if len(matches) == 0:
            return None
        return matches[0]

    def update_status_active_match(
        self,
        line_group_id: str,
        status: int,
    ) -> Match:
        current = self.get_current(line_group_id)

        if current is None:
            return None
        
        match_repository.update(
            {'_id': current._id},
            {'status': status},
        )

        print(
            f'{STATUS_LIST[status]} match: _id={current._id}'
        )

        current.status = status
        return current

    def add_or_drop_tip_score(
        self,
        line_group_id: str,
        line_user_id: str,
        tip_score: Optional[int],
    ) -> Match:
        if line_user_id is None:
            raise ValueError('fail to add_or_drop_tip_score: line_user_id is required')

        matches = match_repository.find({
            'line_group_id': line_group_id,
            'status': 1,
        })

        if len(matches) == 0:
            raise ValueError('Not found match')

        target = matches[0]
        tip_scores = target.tip_scores

        if tip_score is None:
            tip_scores.pop(line_user_id, None)
        else:
            tip_scores[line_user_id] = tip_score

        match_repository.update(
            {'_id': target._id},
            {'tip_scores': tip_scores}
        )

        target.tip_scores = tip_scores

        return target
