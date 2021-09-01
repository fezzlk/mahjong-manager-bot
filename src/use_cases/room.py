"""room"""

from enum import Enum
from repositories import session_scope
from repositories.rooms import RoomsRepository
from repositories.users import UsersRepository
from server import logger
from services import (
    reply_service,
    matches_service,
    app_service,
    hanchans_service,
)


class Modes(Enum):
    """mode"""

    wait = 'wait'
    input = 'input'


class RoomService:
    """room service"""

    def __init__(self):
        self.modes = Modes

    def register(self):
        """register"""

        room_id = app_service.req_room_id
        if room_id is None:
            logger.warning(f'{room_id} is not found')
            return

        with session_scope() as session:
            room = RoomsRepository.find_by_room_id(session, room_id)

            if room is None:
                room = RoomsRepository.create(room_id, self.modes.wait.value)

            logger.info(f'create: {room_id}')

    def chmod(self, mode):
        room_id = app_service.req_room_id
        if mode not in self.modes:
            reply_service.add_message(
                'error: 予期しないモード変更リクエストを受け取りました。')
            return

        with session_scope() as session:
            target = RoomsRepository.find_by_room_id(session, room_id)

            if target is None:
                return

            target.mode = mode.value

            if mode == self.modes.input:
                reply_service.add_message(
                    f'第{matches_service.count_results()+1}回戦お疲れ様です。各自点数を入力してください。\
                    \n（同点の場合は上家が高くなるように数点追加してください）')
                return
            else:
                hanchans_service.disable()
            if mode == self.modes.wait:
                reply_service.add_message(
                    '始める時は「_start」と入力してください。')
                return

    def get_mode(self):
        room_id = app_service.req_room_id

        with session_scope() as session:
            target = RoomsRepository.find_by_room_id(session, room_id)

            if target is None:
                logger.warning(
                    'failed to get mode because room is not found'
                )

                return room_id

            return target.mode

    def get(self, ids=None):
        with session_scope() as session:
            if ids is None:
                return RoomsRepository.find_all(session)

            return RoomsRepository.find_by_ids(session, ids)

    def delete(self, ids):
        with session_scope() as session:
            RoomsRepository.delete_by_ids(session, ids)

        logger.info(f'delete: id={ids}')

    def set_zoom_url(self, zoom_url=None):
        with session_scope() as session:
            if zoom_url is None:
                user_id = app_service.req_user_id
                user = UsersRepository.find_by_user_id(session, user_id)

                if user is None:
                    logger.warning(
                        f'set_zoom_url: user(id={user_id}) is not found')
                    return

                zoom_url = user.zoom_id

            room_id = app_service.req_room_id
            target = RoomsRepository.find_by_room_id(session, room_id)

            if target is None:
                logger.warning(
                    f'set_zoom_url: room(id={room_id}) is not found')
                return

            target.zoom_url = zoom_url

            logger.info(f'set_zoom_url: {zoom_url} to {room_id}')
            reply_service.add_message(
                'Zoom URL を登録しました。\n「_zoom」で呼び出すことができます。')

    def reply_zoom_url(self):
        room_id = app_service.req_room_id

        with session_scope() as session:
            target = RoomsRepository.find_by_room_id(session, room_id)

            if target is None:
                logger.warning(
                    f'reply_zoom_url: room(id={room_id}) is not found')
                return

            if target.zoom_url is None:
                reply_service.add_message(
                    'Zoom URL が登録されていません。URLを送信して下さい。')
                return

            reply_service.add_message(target.zoom_url)
