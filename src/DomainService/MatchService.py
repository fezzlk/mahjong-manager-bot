# from typing import Optional
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

    # def add_hanchan_id(
    #     self,
    #     line_group_id: str,
    #     hanchan_id: int,
    # ) -> Match:
    #     with session_scope() as session:
    #         target = match_repository.find_and_status(
    #             session=session,
    #             line_group_id=line_group_id,
    #             status=1,
    #         )

    #         if target is None:
    #             raise ValueError('Not found match')

    #         hanchan_ids = target.hanchan_ids
    #         hanchan_ids.append(hanchan_id)

    #         updated_match = match_repository.update_one_hanchan_ids_by_id(
    #             session=session,
    #             match_id=target._id,
    #             hanchan_ids=list(set(hanchan_ids)),
    #         )

    #         print(
    #             f'add hanchan id to match: match_id={updated_match._id}'
    #         )

    #         return updated_match

    # def update_hanchan_ids_of_current(self, hanchan_ids, line_group_id):
    #     with session_scope() as session:
    #         target = match_repository.find_and_status(
    #             session=session,
    #             line_group_id=line_group_id,
    #             status=1,
    #         )

    #         if target is None:
    #             raise ValueError('Not found match')

    #         target.hanchan_ids = hanchan_ids

    #         updated_match = match_repository.update_one_hanchan_ids_by_id(
    #             session=session,
    #             match_id=target._id,
    #             hanchan_ids=hanchan_ids,
    #         )
    #         print(
    #             f'update hanchan ids of match: match_id={updated_match._id}'
    #         )
    #         return updated_match

    # def update_current_status(
    #     self,
    #     line_group_id: str,
    #     status: int,
    # ) -> Match:
    #     with session_scope() as session:
    #         target = match_repository.find_and_status(
    #             session=session,
    #             line_group_id=line_group_id,
    #             status=1,
    #         )

    #         if target is None:
    #             raise ValueError('Not found match')

    #         updated_match = match_repository.update_one_status_by_id(
    #             session=session,
    #             match_id=target._id,
    #             status=status,
    #         )

    #         print(
    #             f'{STATUS_LIST[updated_match.status]} match: _id={updated_match._id}'
    #         )

    #         return updated_match

    # def archive(self, line_group_id: str) -> Match:
    #     return self.update_current_status(line_group_id, 2)

    # def disable(self, line_group_id: str) -> Match:
    #     return self.update_current_status(line_group_id, 0)

    # def remove_hanchan_id(
    #     self,
    #     match_id: int,
    #     hanchan_id: int,
    # ) -> Match:
    #     with session_scope() as session:
    #         target = match_repository.find(
    #             session=session,
    #             ids=[match_id],
    #         )

    #         if len(target) == 0:
    #             raise ValueError('Not found match')

    #         hanchan_ids = target[0].hanchan_ids
    #         if hanchan_id in hanchan_ids:
    #             hanchan_ids.remove(hanchan_id)

    #         updated_match = match_repository.update_one_hanchan_ids_by_id(
    #             session=session,
    #             match_id=target[0]._id,
    #             hanchan_ids=hanchan_ids,
    #         )

    #         return updated_match

    # def add_or_drop_tip_score(
    #     self,
    #     line_group_id: str,
    #     line_user_id: str,
    #     tip_score: Optional[int],
    # ) -> Match:
    #     with session_scope() as session:
    #         if line_user_id is None:
    #             raise ValueError('line_user_id is required')

    #         target = match_repository.find_and_status(
    #             session=session,
    #             line_group_id=line_group_id,
    #             status=1,
    #         )

    #         if target is None:
    #             raise ValueError('Not found match')

    #         tip_scores = target.tip_scores

    #         if tip_score is None:
    #             tip_scores.pop(line_user_id, None)
    #         else:
    #             tip_scores[line_user_id] = tip_score

    #         target.tip_scores = tip_scores

    #         match_repository.update(
    #             session=session,
    #             target=target,
    #         )

    #         return target
