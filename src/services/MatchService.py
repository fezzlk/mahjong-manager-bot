"""matches"""

from repositories import session_scope, match_repository
from domains.Match import Match
from server import logger

STATUS_LIST = ['disabled', 'active', 'archived']


class MatchService:
    """match service"""

    def get_or_create_current(self, line_room_id):
        current = self.get_current(line_room_id)

        if current is None:
            self.create(line_room_id)
            current = self.get_current(line_room_id)

        return current

    def get_current(self, line_room_id):
        with session_scope() as session:
            return match_repository.find_one_by_line_room_id_and_status(
                session=session,
                line_room_id=line_room_id,
                status=1,
            )

    def create(self, line_room_id):
        with session_scope() as session:
            new_match = Match(
                line_room_id=line_room_id,
                hanchan_ids=[],
                status=1,
            )
            match_repository.create(session, new_match)

            logger.info(f'create match: room "{line_room_id}"')
            return new_match

    def add_hanchan_id(self, line_room_id, hanchan_id):
        with session_scope() as session:
            record = match_repository.add_hanchan_id_by_line_room_id(
                session=session,
                line_room_id=line_room_id,
                hanchan_id=hanchan_id,
            )

            logger.info(f'update result of match: id={record._id}')

            return record

    def update_hanchan_ids(self, hanchan_ids, line_room_id):
        with session_scope() as session:
            match = match_repository.update_one_hanchan_ids_by_line_room_id(
                session=session,
                line_room_id=line_room_id,
                hanchan_ids=hanchan_ids,
            )
            logger.info(
                f'update hanchan ids of match: match_id={match.id}'
            )
            return match

    def count_results(self, line_room_id):
        current = self.get_current(line_room_id)
        if current is None:
            logger.warning(
                'current match is not found'
            )
            return 0
        return len(current.hanchan_ids)

    def update_status(self, line_room_id, status):
        with session_scope() as session:
            record = match_repository.update_one_status_by_line_room_id(
                session,
                line_room_id,
                status,
            )

            logger.info(
                f'{STATUS_LIST[status]} match: id={record._id}'
            )

            return record

    def archive(self, line_room_id):
        return self.update_status(line_room_id, 2)

    def disable(self, line_room_id):
        return self.update_status(line_room_id, 0)

    def get_archived(self, room_id):
        with session_scope() as session:
            matches = match_repository.find_many_by_room_id_and_status(
                session, room_id, 2)
            if len(matches) == 0:
                return None
            return matches

    def get(self, target_ids):
        with session_scope() as session:
            if target_ids is None:
                return match_repository.find_all(session)
            else:
                return match_repository.find_by_ids(session, target_ids)

    def remove_hanchan_id(self, match_id, hanchan_id):
        with session_scope() as session:
            match = match_repository.remove_hanchan_id_by_id(
                session=session,
                match_id=match_id,
                hanchan_id=hanchan_id,
            )

            return match

    def delete(self, target_ids):
        with session_scope() as session:
            targets = match_repository.find_by_ids(session, target_ids)
            for target in targets:
                session.delete(target)
            logger.info(f'delete: id={target_ids}')
            return targets
