# flake8: noqa: E999
"""matches"""

from repositories import session_scope
from repositories.matches import MatchesRepository

import json
from server import logger

STATUS_LIST = ['disabled', 'active', 'archived']


class MatchesService:
    """matches service"""

    def get_or_add_current(self, room_id):
        current = self.get_current(room_id)

        if current is None:
            current = self.create(room_id)

        return current

    def get_current(self, room_id):
        with session_scope() as session:
            return MatchesRepository.find_by_room_id_and_status(
                session, room_id, 1)

    def create(self, room_id):
        with session_scope() as session:
            match = MatchesRepository.create(session, room_id)

            logger.info(f'create match: to room "{room_id}"')
            return match

    def add_result(self, room_id, result_id):
        with session_scope():
            current_match = self.get_current(room_id)
            if current_match is None:
                current_match = self.create(room_id)

            result_ids = json.loads(current_match.result_ids)
            result_ids.append(str(result_id))
            current_match.result_ids = json.dumps(result_ids)

        logger.info(f'update result of match: id={current_match.id}')

    def update_hanchan_ids(self, result_ids):
        with session_scope():
            current = self.get_current()
            current.result_ids = json.dumps(result_ids)
            logger.info(
                f'update hanchan ids of match: match_id={current.id}'
            )

    def count_results(self):
        current = self.get_current()
        if current is None:
            logger.warning(
                'current match is not found'
            )
            return 0
        return len(json.loads(current.result_ids))

    def update_status(self, room_id, status):
        with session_scope as session:
            current = MatchesRepository.find_by_room_id_and_status(
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
            matches = MatchesRepository.find_many_by_room_id_and_status(
                session, room_id, 2)
            if len(matches) == 0:
                return None
            return matches

    def get(self, target_ids):
        with session_scope as session:
            if target_ids is None:
                return MatchesRepository.find_all(session)
            else:
                return MatchesRepository.find_by_ids(session, target_ids)

    def remove_hanchan_id(self, match_id, result_id):
        with session_scope as session:
            match = MatchesRepository.find_by_ids(session, match_id)
            result_ids = json.loads(match.result_ids)
            if result_id in result_ids:
                result_ids.remove(result_id)
            match.result_ids = json.dumps(result_ids)

    def delete(self, target_ids):
        with session_scope as session:
            targets = MatchesRepository.find_by_ids(session, target_ids)
            for target in targets:
                session.delete(target)
            logger.info(f'delete: id={target_ids}')
            return targets
