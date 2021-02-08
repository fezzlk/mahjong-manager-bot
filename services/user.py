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

    def register(self, profile=None):
        """register"""
        if profile is None:
            profile = self.services.app_service.line_bot_api.get_profile(
                self.services.app_service.req_user_id
            )
        target = self.services.app_service.db.session\
            .query(Users).filter(Users.user_id == profile.user_id).all()
        if len(target) == 0:
            self.services.app_service.logger.info('create a user record')
            user = Users(name=profile.display_name,
                         user_id=profile.user_id,
                         mode=self.modes.wait.value,
                         )
            self.services.app_service.db.session.add(user)
            self.services.app_service.db.session.commit()
        return profile

    def get_name(self):
        profile = self.services.app_service.line_bot_api.get_profile(
            self.services.app_service.req_user_id
        )
        return profile.display_name

    def delete(self, user_id):
        """delete"""
        self.services.app_service.logger.info('delete a user record')
        self.services.app_service.db.session.query(Users).\
            filter(Users.user_id == user_id).\
            delete()
        self.services.app_service.db.session.commit()

    def update(self, profile):
        target = self.services.app_service.db.session\
            .query(Users).filter(Users.user_id == profile.user_id).first()
        if target == None:
            return
        target.name = profile.display_name
        self.services.app_service.db.session.commit()

    def chmod(self, mode):
        user_id = self.services.app_service.req_user_id
        if not mode in self.modes:
            self.services.reply_service.add_text(
                'error: 予期しないモード変更リクエストを受け取りました。')
            return

        target = self.services.app_service.db.session\
            .query(Users).filter(Users.user_id == user_id).first()
        if target == None:
            return
        target.mode = mode.value
        self.services.app_service.db.session.commit()

        if mode == self.modes.wait:
            self.services.reply_service.add_text(
                f'こんにちは。快適な麻雀生活の提供に努めます。今日のラッキー牌は「{self.services.app_service.get_random_hai()}」です。')

    def get_mode(self):
        user_id = self.services.app_service.req_user_id
        target = self.services.app_service.db.session\
            .query(Users).filter(Users.user_id == user_id).first()
        if target == None:
            return
        return target.mode

    def reply_mode(self):
        self.services.reply_service.add_text(self.get_mode())

    def reply_all(self):
        self.services.reply_service.add_text(
            '\n'.join([user.name for user in self.get_all()])
        )

    def get_all(self):
        return self.services.app_service.db.session\
            .query(Users)\
            .order_by(Users.id)\
            .all()

    def delete(self, target_ids):
        if type(target_ids) != list:
            target_ids = [target_ids]
        self.services.app_service.db.session\
            .query(Users).filter(
                Users.id.in_(target_ids),
            ).delete(synchronize_session=False)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'delete: id={target_ids}')
