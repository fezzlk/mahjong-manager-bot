"""user"""

from enum import Enum
from repositories import session_scope
from repositories.users import UsersRepository


class Modes(Enum):
    """mode"""

    wait = 'wait'


class UserService:
    """user service"""

    def __init__(self, services):
        self.services = services
        self.modes = Modes

    def register(self):
        """register"""
        profile = self.services.app_service.line_bot_api.get_profile(
            self.services.app_service.req_user_id
        )

        with session_scope() as session:
            target = UsersRepository.find_by_user_id(session, profile.user_id)

        if target is None:
            target = self.create(profile.display_name, profile.user_id)

        return target

    def get_name_by_user_id(self, user_id=None):
        if user_id is None:
            user_id = self.services.app_service.req_user_id

        try:
            profile = self.services.app_service.line_bot_api.get_profile(
                user_id)

            return profile.display_name

        except Exception as err:
            with session_scope() as session:
                target = UsersRepository.find_by_user_id(session, user_id)
            
                if target is None:
                    self.services.app_service.logger.warning(f'user({user_id}) is not found')
                    return user_id
                else:
                    return target.name

    def get_user_id_by_name(self, name):
        with session_scope() as session:
            target = UsersRepository.find_by_name(session, name)

            if target is None:
                self.services.app_service.logger.warning(f'user({name}) is not found')
                return name
                
            return target.user_id

    def delete_by_user_id(self, user_id):
        """delete"""
        with session_scope() as session:
            UsersRepository.delete_by_user_id(session, user_id)

        self.services.app_service.logger.info(f'delete: {user_id}')

    def chmod(self, mode):
        user_id = self.services.app_service.req_user_id
        if mode not in self.modes:
            raise BaseException(f'予期しないモード変更リクエストを受け取りました。\'{mode}\'')

        with session_scope() as session:
            target = UsersRepository.find_by_user_id(session, user_id)

            if target is None:
                self.services.app_service.logger.warning(f'user is not found: {user_id}')
                self.services.reply_service.add_message(
                    'ユーザーを認識できませんでした。当アカウントをブロック、ブロック解除してください'
                )

            target.mode = mode.value

        self.services.app_service.logger.info(f'chmod: {user_id}: {mode}')

    def get_mode(self):
        user_id = self.services.app_service.req_user_id
        with session_scope() as session:
            target = UsersRepository.find_by_user_id(session, user_id)

            if target is None:
                self.services.app_service.logger.warning(f'user is not found: {user_id}')
                self.services.reply_service.add_message(
                    'ユーザーを認識できませんでした。当アカウントを一度ブロックし、ブロック解除してください'
                )
                return

            return target.mode

    def reply_mode(self):
        self.services.reply_service.add_message(self.get_mode())

    def get(self, ids=None):
        with session_scope() as session:
            if target_ids is None:
                return UsersRepository.find_all(session)
            
            return UsersRepository.find_by_ids(session, ids)

    def delete(self, ids):
        with session_scope() as session:
            UsersRepository.delete_by_ids(session, ids)

        self.services.app_service.logger.info(f'delete: id={target_ids}')

    def create(self, name, user_id):
        with session_scope() as session:
            new_user = UsersRepository.create(name, user_id, self.modes.wait.value)
            self.services.app_service.logger.info(f'create: {new_user.user_id} {new_user.name}')
            return new_user

    def set_zoom_id(self, zoom_id):
        user_id = self.services.app_service.req_user_id
        with session_scope() as session:
            target = UsersRepository.find_by_user_id(session, user_id)

            if target is None:
                self.services.app_service.logger.warning(f'set_zoom_url: user(id={user_id}) is not found')
                return
                
            target.zoom_id = zoom_id

            self.services.app_service.logger.info(f'set_user_url: {zoom_id} to {user_id}')
            self.services.reply_service.add_message(
                f'Zoom URL を登録しました。\nトークルームにて「_my_zoom」で呼び出すことができます。')

    def reply_zoom_id(self):
        user_id = self.services.app_service.req_user_id

        with session_scope() as session:
            target = UsersRepository.find_by_user_id(session, user_id)

            if target is None:
                self.services.app_service.logger.warning(f'reply_zoom_url: user(id={user_id}) is not found')
                return

            if target.zoom_id is None:
                self.services.reply_service.add_message(
                    f'Zoom URL が登録されていません。個人チャットの設定から登録してください。')
                return
                
            self.services.reply_service.add_message(target.zoom_id)
            return
