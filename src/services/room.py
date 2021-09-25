# flake8: noqa: E999
from enum import Enum
from domains.Room import Room, RoomMode
from repositories import session_scope, room_repository
from server import logger


class Modes(Enum):
    """mode"""

    wait = 'wait'
    input = 'input'


class RoomService:
    """room service"""

    def __init__(self):
        self.modes = Modes

    def find_or_create(self, room_id):
        with session_scope() as session:
            room = room_repository.find_one_by_room_id(session, room_id)

            if room is None:
                new_room = Room(
                    line_room_id=room_id,
                    zoom_url=None,
                    mode=RoomMode.wait.value,
                    users=[],
                )
                room = room_repository.create(new_room)
                logger.info(f'create room: {room_id}')

            return room

    def chmod(self, room_id, mode):
        if mode not in self.modes:
            logger.warning(
                'failed to change mode: unexpected mode request received.'
            )
            return None

        with session_scope() as session:
            target = room_repository.find_one_by_room_id(session, room_id)

            if target is None:
                logger.warning(
                    'failed to change mode: room is not found'
                )
                return None

            target.mode = mode.value
            return target.mode

    def get_mode(self, room_id):
        with session_scope() as session:
            target = room_repository.find_one_by_room_id(session, room_id)

            if target is None:
                logger.warning(
                    'failed to get mode: room is not found'
                )

                return None

            return target.mode

    def get(self, ids=None):
        with session_scope() as session:
            if ids is None:
                return room_repository.find_all(session)

            return room_repository.find_by_ids(session, ids)

    def delete(self, ids):
        with session_scope() as session:
            room_repository.delete_by_ids(session, ids)

        logger.info(f'delete: id={ids}')

    def set_zoom_url(self, room_id, zoom_url):
        with session_scope() as session:
            target = room_repository.find_one_by_room_id(session, room_id)

            if target is None:
                logger.warning(
                    f'fail to set zoom url: room "{room_id}" is not found')
                return None

            target.zoom_url = zoom_url

            logger.info(f'set_zoom_url: {zoom_url} to {room_id}')
            return zoom_url

    def get_zoom_url(self, room_id):
        with session_scope() as session:
            target = room_repository.find_one_by_room_id(session, room_id)

            if target is None:
                logger.warning(
                    f'fail to get zoom url: room "{room_id}" is not found.')
                return None

            if target.zoom_url is None:
                logger.warning(
                    f'fail to get zoom url: room "{room_id}" does not have zoom url.')
                return None

            return target.zoom_url
