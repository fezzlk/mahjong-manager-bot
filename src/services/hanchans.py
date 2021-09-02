"""hanchans"""

import json
from repositories import session_scope
from repositories.hanchans import HanchansRepository
from server import logger
from services import (
    app_service,
    matches_service,
    reply_service,
    user_service,
    message_service,
    config_service,
)
STATUS_LIST = ['disabled', 'active', 'archived']


class HanchansService:
    """Hanchans service"""

    def add(self, raw_scores={}, room_id, current_match):
        with session_scope() as session:
            HanchansRepository.create(
                session,
                room_id,
                current_match.id,
                raw_scores
            )

        logger.info(
            f'create hanchan: to room "{room_id}"'
        )

    def delete_by_id(self, room_id, target_id):
        """disabled target hanchan"""
        with session_scope() as session:
            target = HanchansRepository.find_by_id_and_room_id(
                session,
                target_id,
                room_id
            )

            target.status = 0
            logger.info(
                f'delete: id={target_id} room_id={room_id}'
            )
            reply_service.add_message(
                f'id={target_id}の結果を削除しました。'
            )

    def find_by_ids(self, ids):
        with session_scope() as session:
            return HanchansRepository.find_by_ids(session, ids)

    def get_current(self, room_id):
        with session_scope as session:
            return HanchansRepository.find_by_room_id_and_status(
                session,
                room_id,
                1
            )

    # 関数名検討
    def add_raw_score(self, room_id, user_id, raw_score):
        with session_scope as session:
            hanchan = HanchansRepository.find_by_room_id_and_status(
                session,
                room_id,
                1
            )

            raw_scores = json.loads(hanchan.raw_scores)
            raw_scores[user_id] = raw_score
            hanchan.raw_scores = json.dumps(raw_scores)
            return raw_scores

    def drop_raw_score(self, room_id, user_id):
        with session_scope as session:
            hanchan = HanchansRepository.find_by_room_id_and_status(
                session,
                room_id,
                1
            )

            raw_scores = json.loads(hanchan.raw_scores)
            if user_id in raw_scores.keys():
                raw_scores.pop(user_id)

            hanchan.raw_scores = json.dumps(raw_scores)
            return raw_scores

    # clear の方がいいのでは
    def reset_raw_scores(self, room_id):
        with session_scope as session:
            hanchan = HanchansRepository.find_by_room_id_and_status(
                session,
                room_id,
                1
            )

            hanchan.raw_scores = json.dumps({})

    # update_converted_score
    def update_hanchan(self, calculated_hanchan):
        with session_scope as session:
            hanchan = HanchansRepository.find_by_room_id_and_status(
                session,
                room_id,
                1
            )

            hanchan.converted_scores = json.dumps(calculated_hanchan)
            logger.info(
                f'update hanchan: id={hanchan.id}'
            )

    # update_status
    def change_status(self, room_id, status):
        with session_scope as session:
            current = HanchansRepository.find_by_room_id_and_status(
                session,
                room_id,
                1
            )

            if current is None:
                return
            current.status = status
            logger.info(
                f'{STATUS_LIST[status]}: id={current.id}'
            )

    def get(self, ids=None):
        with session_scope as session:
            if ids is None:
                targets = HanchansRepository.find_all(session)
            else:
                targets = HanchansRepository.find_by_ids(session, ids)

            for hanchan in targets:
                if hanchan.raw_scores is not None:
                    hanchan.raw_scores = json.loads(hanchan.raw_scores)

                if hanchan.converted_scores is not None:
                    hanchan.converted_scores = json.loads(
                        hanchan.converted_scores
                    )

            return targets

    def delete(self, ids):
        with session_scope as session:
            targets = HanchansRepository.find_by_ids(session, ids)

            for target in targets:
                matches_service.remove_hanchan_id(
                    target.match_id, target.id)
                session.delete(target)

            logger.info(f'delete: id={ids}')

    def migrate(self):
        with session_scope as session:
            targets = HanchansRepository.find_all(session)

            for t in targets:
                raw_scores = json.loads(t.raw_scores)

                new_raw_scores = {}
                for k, v in raw_scores.items():
                    user_id = user_service.get_user_id_by_name(k)
                    new_raw_scores[user_id] = v
                t.raw_scores = json.dumps(new_raw_scores)

                if t.converted_scores is not None:
                    converted_scores = json.loads(t.converted_scores)

                    new_converted_scores = {}
                    for k, v in converted_scores.items():
                        user_id = user_service.get_user_id_by_name(k)
                        new_converted_scores[user_id] = v

                    t.converted_scores = json.dumps(new_converted_scores)
