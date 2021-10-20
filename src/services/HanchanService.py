import json
from typing import Dict, List
from repositories import session_scope, hanchan_repository
from server import logger
from domains.Hanchan import Hanchan
from domains.Match import Match
from .interfaces.IHanchanService import IHanchanService

STATUS_LIST = ['disabled', 'active', 'archived']


class HanchanService(IHanchanService):
    def create(
        self,
        raw_scores: Dict[str, int],
        line_room_id: str,
        related_match: Match,
    ) -> Hanchan:
        new_hanchan = Hanchan(
            line_room_id=line_room_id,
            raw_scores=raw_scores,
            converted_scores='',
            match_id=related_match._id,
            status=1,
        )
        with session_scope() as session:
            hanchan_repository.create(
                session,
                new_hanchan,
            )

        logger.info(
            f'create hanchan: to room "{line_room_id}"'
        )

        return new_hanchan

    def disabled_by_id(
        self,
        line_room_id: str, 
        hanchan_id: int,
    ) -> Hanchan:
        """disabled target hanchan"""
        with session_scope() as session:
            new_hanchan = hanchan_repository.update_status_by_id_and_line_room_id(
                session,
                hanchan_id=hanchan_id,
                line_room_id=line_room_id,
                status=0,
            )

            logger.info(
                f'disabled: id={hanchan_id}'
            )

            return new_hanchan

    def find_by_ids(
        self,
        ids: List[str],
    ) -> List[Hanchan]:
        with session_scope() as session:
            return hanchan_repository.find_by_ids(session, ids)

    def get_current(self, line_room_id):
        with session_scope as session:
            return hanchan_repository.find_one_by_line_room_id_and_status(
                session,
                line_room_id,
                1
            )

    def add_raw_score(
        self,
        line_room_id: str,
        line_user_id: str,
        raw_score: int,
    ) -> Hanchan:
        with session_scope() as session:
            hanchan = hanchan_repository.update_raw_score_of_user_by_room_id(
                session=session,
                line_room_id=line_room_id,
                line_user_id=line_user_id,
                raw_score=raw_score,
            )

            return hanchan

    def drop_raw_score(
        self,
        line_room_id: str,
        line_user_id: str,
    ) -> Hanchan:
        with session_scope() as session:
            hanchan = hanchan_repository.update_raw_score_of_user_by_room_id(
                session=session,
                line_room_id=line_room_id,
                line_user_id=line_user_id,
                raw_score=None,
            )

            return hanchan

    def update_converted_score(
        self,
        line_room_id: str,
        converted_scores: Dict[str, int],
    ) -> Hanchan:
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

    def update_status(
        self,
        line_room_id: str,
        status: int,
    ) -> Hanchan:
        with session_scope() as session:
            hanchan = hanchan_repository.update_status_by_line_room_id(
                session,
                line_room_id,
                status,
            )

            logger.info(
                f'{STATUS_LIST[status]} hanchan: id={hanchan._id}'
            )

            return hanchan

    def archive(self, line_room_id: str) -> Hanchan:
        return self.update_status(line_room_id, 2)

    def disable(self, line_room_id: str) -> Hanchan:
        return self.update_status(line_room_id, 0)

    def get(self, ids: List[int] = None) -> List[Hanchan]:
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

    def delete(self, ids: List[int]) -> List[Hanchan]:
        with session_scope() as session:
            targets = hanchan_repository.find_by_ids(session, ids)
            for target in targets:
                session.delete(target)

            logger.info(f'delete: id={ids}')
            return targets
