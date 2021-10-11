# flake8: noqa: E999
"""matches"""

from repositories import session_scope, match_repository
from domains.Match import Match
import json
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

    def get_current(self, room_id):
        with session_scope() as session:
            return match_repository.find_one_by_line_room_id_and_status(
                session, room_id, 1)

    def create(self, line_room_id):
        with session_scope() as session:
            new_match = Match(
                line_room_id=line_room_id,
                hanchan_ids=[],
                status=1,
            )
            match = match_repository.create(session, new_match)

            logger.info(f'create match: to room "{line_room_id}"')
            return match

    def add_hanchan_id(self, line_room_id, hanchan_id):
        with session_scope() as session:
            record = match_repository.add_hanchan_id_by_line_room_id(
                session=session,
                line_room_id=line_room_id,
                hanchan_id=hanchan_id,
            )

            logger.info(f'update result of match: id={record._id}')

            return record

    def update_hanchan_ids(self, result_ids, room_id):
        with session_scope():
            current = self.get_current(room_id)
            current.result_ids = json.dumps(result_ids)
            logger.info(
                f'update hanchan ids of match: match_id={current.id}'
            )

    def count_results(self, room_id):
        current = self.get_current(room_id)
        if current is None:
            logger.warning(
                'current match is not found'
            )
            return 0
        return len(json.loads(current.hanchan_ids))

    def update_status(self, room_id, status):
        with session_scope as session:
            current = match_repository.find_one_by_line_room_id_and_status(
                session,
                room_id,
                1
            )

            if current is None:
                return
            current.status = status
            logger.info(
                f'{STATUS_LIST[status]} match: id={current.id}'
            )

    def archive(self):
        self.update_status(2)

    def disable(self):
        self.update_status(0)

    def get_archived(self, room_id):
        with session_scope as session:
            matches = match_repository.find_many_by_room_id_and_status(
                session, room_id, 2)
            if len(matches) == 0:
                return None
            return matches

    def get(self, target_ids):
        with session_scope as session:
            if target_ids is None:
                return match_repository.find_all(session)
            else:
                return match_repository.find_by_ids(session, target_ids)

    def remove_hanchan_id(self, match_id, result_id):
        with session_scope as session:
            match = match_repository.find_by_ids(session, match_id)
            result_ids = json.loads(match.result_ids)
            if result_id in result_ids:
                result_ids.remove(result_id)
            match.result_ids = json.dumps(result_ids)

    def delete(self, target_ids):
        with session_scope as session:
            targets = match_repository.find_by_ids(session, target_ids)
            for target in targets:
                session.delete(target)
            logger.info(f'delete: id={target_ids}')
            return targets
