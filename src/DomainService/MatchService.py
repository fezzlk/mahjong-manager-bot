from .interfaces.IMatchService import IMatchService
from repositories import session_scope, match_repository
from DomainModel.entities.Match import Match

STATUS_LIST = ['disabled', 'active', 'archived']


class MatchService(IMatchService):

    def get_or_create_current(self, line_group_id: str) -> Match:
        current = self.get_current(line_group_id)

        if current is None:
            with session_scope() as session:
                new_match = Match(
                    line_group_id=line_group_id,
                    hanchan_ids=[],
                    status=1,
                )
                match_repository.create(session, new_match)

                print(f'create match: group "{line_group_id}"')
                current = new_match

        return current

    def get_current(self, line_group_id: str) -> Match:
        with session_scope() as session:
            return match_repository.find_one_by_line_group_id_and_status(
                session=session,
                line_group_id=line_group_id,
                status=1,
            )

    def add_hanchan_id(
        self,
        line_group_id: str,
        hanchan_id: int,
    ) -> Match:
        with session_scope() as session:
            target = match_repository.find_one_by_line_group_id_and_status(
                session=session,
                line_group_id=line_group_id,
                status=1,
            )

            if target is None:
                raise ValueError('Not found match')

            hanchan_ids = target.hanchan_ids
            hanchan_ids.append(hanchan_id)

            updated_match = match_repository.update_one_hanchan_ids_by_id(
                session=session,
                match_id=target._id,
                hanchan_ids=list(set(hanchan_ids)),
            )

            print(
                f'add hanchan id to match: match_id={updated_match._id}'
            )

            return updated_match

    def update_hanchan_ids_of_current(self, hanchan_ids, line_group_id):
        with session_scope() as session:
            target = match_repository.find_one_by_line_group_id_and_status(
                session=session,
                line_group_id=line_group_id,
                status=1,
            )

            if target is None:
                raise ValueError('Not found match')

            target.hanchan_ids = hanchan_ids

            updated_match = match_repository.update_one_hanchan_ids_by_id(
                session=session,
                match_id=target._id,
                hanchan_ids=hanchan_ids,
            )
            print(
                f'update hanchan ids of match: match_id={updated_match._id}'
            )
            return updated_match

    def update_current_status(
        self,
        line_group_id: str,
        status: int,
    ) -> Match:
        with session_scope() as session:
            target = match_repository.find_one_by_line_group_id_and_status(
                session=session,
                line_group_id=line_group_id,
                status=1,
            )

            if target is None:
                raise ValueError('Not found match')

            updated_match = match_repository.update_one_status_by_id(
                session=session,
                match_id=target._id,
                status=status,
            )

            print(
                f'{STATUS_LIST[updated_match.status]} match: id={updated_match._id}'
            )

            return updated_match

    def archive(self, line_group_id: str) -> Match:
        return self.update_current_status(line_group_id, 2)

    def disable(self, line_group_id: str) -> Match:
        return self.update_current_status(line_group_id, 0)

    def remove_hanchan_id(
        self,
        match_id: int,
        hanchan_id: int,
    ) -> Match:
        with session_scope() as session:
            target = match_repository.find_by_ids(
                session=session,
                ids=[match_id],
            )

            if len(target) == 0:
                raise ValueError('Not found match')

            hanchan_ids = target[0].hanchan_ids
            if hanchan_id in hanchan_ids:
                hanchan_ids.remove(hanchan_id)

            updated_match = match_repository.update_one_hanchan_ids_by_id(
                session=session,
                match_id=target[0]._id,
                hanchan_ids=hanchan_ids,
            )

            return updated_match
