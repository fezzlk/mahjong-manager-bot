from repositories import hanchan_repository
from DomainModel.entities.Hanchan import Hanchan
from .interfaces.IHanchanService import IHanchanService
from typing import Optional

STATUS_LIST = ['disabled', 'active', 'archived']


class HanchanService(IHanchanService):

    def add_or_drop_raw_score(
        self,
        line_group_id: str,
        line_user_id: str,
        raw_score: Optional[int],
    ) -> Hanchan:
        if line_user_id is None:
            raise ValueError('fail to add_or_drop_raw_score: line_user_id is required')

        result = hanchan_repository.find({
            'line_group_id': line_group_id,
            'status': 1,
        })

        if len(result) == 0:
            raise ValueError('fail to add_or_drop_raw_score: Not found hanchan')

        target = result[0]
        raw_scores = target.raw_scores

        if raw_score is None:
            raw_scores.pop(line_user_id, None)
        else:
            raw_scores[line_user_id] = raw_score

        hanchan_repository.update(
            {'_id': target._id},
            {'raw_scores': raw_scores},
        )

        target.raw_scores = raw_scores
        return target

    def update_status_active_hanchan(
        self,
        line_group_id: str,
        status: int,
    ) -> None:
        update_count = hanchan_repository.update(
            {
                'status': 1,
                'line_group_id': line_group_id,
            },
            {'status': status},
        )

        if update_count > 0:
            print(
                f'Change hanchan status in group({line_group_id}) to {STATUS_LIST[status]}'
            )

    # def find_or_create_current(self, line_group_id: str, match_id) -> Hanchan:
    #     current = self.get_current(line_group_id)

    #     if current is None:
    #         new_hanchan = Hanchan(
    #             line_group_id=line_group_id,
    #             match_id=match_id,
    #             status=1,
    #         )
    #         hanchan_repository.create(new_hanchan)

    #         print(f'create hanchan: group "{line_group_id}"')
    #         current = new_hanchan

    #     return current

    def get_current(self, line_group_id: str) -> Hanchan:
        hanchans = hanchan_repository.find({
            '$and': [
                {'line_group_id': line_group_id},
                {'status': 1},
            ]
        })
        
        if len(hanchans) == 0:
            return None
        return hanchans[0]
