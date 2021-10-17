"""hanchans"""

import json
from repositories import session_scope, hanchan_repository
from server import logger
from domains.Hanchan import Hanchan

STATUS_LIST = ['disabled', 'active', 'archived']


class HanchanService:
    """Hanchans service"""

    def create(self, raw_scores, room_id, current_match):
        new_hanchan = Hanchan(
            line_room_id=room_id,
            raw_scores=raw_scores,
            converted_scores='',
            match_id=current_match._id,
            status=1,
        )
        with session_scope() as session:
            hanchan_repository.create(
                session,
                new_hanchan,
            )

        logger.info(
            f'create hanchan: to room "{room_id}"'
        )

    def disabled_by_id(self, line_room_id, hanchan_id):
        """disabled target hanchan"""
        with session_scope() as session:
            hanchan_repository.update_status_by_id_and_line_room_id(
                session,
                hanchan_id=hanchan_id,
                line_room_id=line_room_id,
                status=0,
            )

            logger.info(
                f'disabled: id={hanchan_id}'
            )

    def find_by_ids(self, ids):
        with session_scope() as session:
            return hanchan_repository.find_by_ids(session, ids)

    def get_current(self, line_room_id):
        with session_scope as session:
            return hanchan_repository.find_one_by_line_room_id_and_status(
                session,
                line_room_id,
                1
            )

    def add_raw_score(self, line_room_id, line_user_id, raw_score):
        with session_scope() as session:
            hanchan = hanchan_repository.update_raw_score_of_user_by_room_id(
                session=session,
                line_room_id=line_room_id,
                line_user_id=line_user_id,
                raw_score=raw_score,
            )

            return hanchan

    def drop_raw_score(self, line_room_id, line_user_id):
        with session_scope() as session:
            hanchan = hanchan_repository.update_raw_score_of_user_by_room_id(
                session=session,
                line_room_id=line_room_id,
                line_user_id=line_user_id,
                raw_score=None,
            )

            return hanchan

    def clear_raw_scores(self, line_room_id):
        with session_scope() as session:
            record = hanchan_repository.update_raw_score_of_user_by_room_id(
                session=session,
                line_room_id=line_room_id,
                line_user_id=None,
                raw_score=None,
            )

            return record

    def update_converted_score(self, line_room_id, converted_scores):
        with session_scope() as session:
            hanchan = hanchan_repository.update_one_converted_score_by_line_room_id(
                session=session,
                line_room_id=line_room_id,
                converted_scores=converted_scores,
            )

            logger.info(
                f'update hanchan: id={hanchan._id}'
            )

            return hanchan

    def change_status(self, room_id, status):
        with session_scope() as session:
            hanchan = hanchan_repository.update_status_by_line_room_id(
                session,
                room_id,
                status,
            )

            logger.info(
                f'{STATUS_LIST[status]} hanchan: id={hanchan._id}'
            )

            return hanchan

    def archive(self, room_id):
        self.change_status(room_id, 2)

    def disable(self, room_id):
        self.change_status(room_id, 0)

    def get(self, ids=None):
        with session_scope() as session:
            if ids is None:
                targets = hanchan_repository.find_all(session)
            else:
                targets = hanchan_repository.find_by_ids(session, ids)

            for hanchan in targets:
                if hanchan.raw_scores is not None:
                    hanchan.raw_scores = json.loads(hanchan.raw_scores)

                if hanchan.converted_scores is not None:
                    hanchan.converted_scores = json.loads(
                        hanchan.converted_scores
                    )

            return targets

    def delete(self, ids):
        with session_scope() as session:
            targets = hanchan_repository.find_by_ids(session, ids)
            for target in targets:
                session.delete(target)

            logger.info(f'delete: id={ids}')
            return targets
