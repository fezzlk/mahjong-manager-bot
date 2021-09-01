"""user"""

from enum import Enum
from repositories import session_scope
from repositories.users import UsersRepository
from server import logger, line_bot_api
from services import app_service


class Modes(Enum):
    """mode"""

    wait = 'wait'


class UserService:
    """user service"""

    def __init__(self):
        self.modes = Modes

    def delete_by_user_id(self, user_id):
        """delete"""
        with session_scope() as session:
            UsersRepository.delete_by_user_id(session, user_id)

        logger.info(f'delete: {user_id}')

    def find_or_create_by_profile(self, profile):
        """find or create by receiving message"""
        with session_scope() as session:
            target = UsersRepository.find_by_user_id(session, profile.user_id)

        if target is None:
            target = self.create(profile.display_name, profile.user_id)

        return target

    def create(self, name, user_id):
        with session_scope() as session:
            new_user = UsersRepository.create(
                session,
                name,
                user_id,
                self.modes.wait.value
            )
            logger.info(f'create: {new_user.user_id} {new_user.name}')
            return new_user

    def delete(self, ids):
        with session_scope() as session:
            UsersRepository.delete_by_ids(session, ids)

        logger.info(f'delete: id={ids}')

    def get(self, ids=None):
        with session_scope() as session:
            if ids is None:
                return UsersRepository.find_all(session)

            return UsersRepository.find_by_ids(session, ids)

    def get_name_by_user_id(self, user_id):
        try:
            profile = line_bot_api.get_profile(
                user_id)

            return profile.display_name

        except Exception:
            with session_scope() as session:
                target = UsersRepository.find_by_user_id(session, user_id)

                if target is None:
                    logger.warning(f'user({user_id}) is not found')
                    return user_id
                else:
                    return target.name

    def get_user_id_by_name(self, name):
        with session_scope() as session:
            target = UsersRepository.find_by_name(session, name)

            if target is None:
                logger.warning(f'user({name}) is not found')
                return name

            return target.user_id

    def chmod(self, user_id, mode):
        if mode not in self.modes:
            raise BaseException(f'予期しないモード変更リクエストを受け取りました。\'{mode}\'')

        with session_scope() as session:
            target = UsersRepository.find_by_user_id(session, user_id)

            if target is None:
                logger.warning(f'user is not found: {user_id}')
                self.services.reply_service.add_message(
                    'ユーザーを認識できませんでした。当アカウントをブロック、ブロック解除してください'
                )

            target.mode = mode.value

        logger.info(f'chmod: {user_id}: {mode}')

    def get_mode(self, user_id):
        with session_scope() as session:
            target = UsersRepository.find_by_user_id(session, user_id)

            if target is None:
                logger.warning(f'user is not found: {user_id}')
                return None

            return target.mode

    def set_zoom_id(self, user_id, zoom_id):
        with session_scope() as session:
            target = UsersRepository.find_by_user_id(session, user_id)

            if target is None:
                logger.warning(f'set_zoom_url: user "{user_id}" is not found')
                return None

            target.zoom_id = zoom_id
        logger.info(f'set_user_url: {zoom_id} to {user_id}')
        return zoom_id

    def get_zoom_id(self, user_id):
        with session_scope() as session:
            target = UsersRepository.find_by_user_id(session, user_id)

            if target is None:
                logger.warning(f'user_services: user "{user_id}" is not found')
                return None

            if target.zoom_id is None:
                logger.warning(
                    f'user_services: zoom id of user "{user_id}" is None')
                return None

            return target.zoom_id
