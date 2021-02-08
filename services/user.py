"""user"""

from enum import Enum
from models import Users


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
        target = self.services.app_service.db.session\
            .query(Users).filter(Users.user_id == profile.user_id).first()
        if target is None:
            target = Users(
                name=profile.display_name,
                user_id=profile.user_id,
                mode=self.modes.wait.value,
            )
            self.services.app_service.db.session.add(target)
            self.services.app_service.db.session.commit()
            self.services.app_service.logger.info(f'create: {profile.user_id} {profile.display_name}')
        return target

    def get_name_by_user_id(self, user_id=None):
        if user_id is None:
            user_id = self.services.app_service.req_user_id
        profile = self.services.app_service.line_bot_api.get_profile(user_id)
        return profile.display_name

    def delete_by_user_id(self, user_id):
        """delete"""
        self.services.app_service.db.session.query(Users).\
            filter(Users.user_id == user_id).\
            delete()
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'delete: {user_id}')

    def chmod(self, mode):
        user_id = self.services.app_service.req_user_id
        if not mode in self.modes:
            raise BaseException(f'予期しないモード変更リクエストを受け取りました。\'{mode}\'')

        target = self.services.app_service.db.session\
            .query(Users).filter(Users.user_id == user_id).first()
        if target == None:
            self.services.app_service.logger.warning(f'user is not found: {user_id}')
            self.services.reply_service.add_text(
                'ユーザーを認識できませんでした。お手数おかけしますが当アカウントをブロック、ブロック解除してください'
            )
        target.mode = mode.value
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'chmod: {user_id}: {mode}')

    def get_mode(self):
        user_id = self.services.app_service.req_user_id
        target = self.services.app_service.db.session\
            .query(Users).filter(Users.user_id == user_id).first()
        if target == None:
            self.services.app_service.logger.warning(f'user is not found: {user_id}')
            self.services.reply_service.add_text(
                'ユーザーを認識できませんでした。お手数おかけしますが当アカウントを一度ブロックし、ブロック解除してください'
            )
            return
        return target.mode

    def reply_mode(self):
        self.services.reply_service.add_text(self.get_mode())

    def get(self, target_ids=None):
        if target_ids is None:
            return self.services.app_service.db.session\
                .query(Users)\
                .order_by(Users.id)\
                .all()
        if type(target_ids) != list:
            target_ids = [target_ids]
        return self.services.app_service.db.session\
            .query(Users).filter(Users.id.in_(target_ids))\
            .order_by(Users.id).all()

    def delete(self, target_ids):
        if type(target_ids) != list:
            target_ids = [target_ids]
        self.services.app_service.db.session\
            .query(Users).filter(
                Users.id.in_(target_ids),
            ).delete(synchronize_session=False)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'delete: id={target_ids}')
