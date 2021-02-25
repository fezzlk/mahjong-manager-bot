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
            target = self.create(profile.display_name, profile.user_id)
        return target

    def get_name_by_user_id(self, user_id=None):
        if user_id is None:
            user_id = self.services.app_service.req_user_id
        print(user_id)
        try:
            profile = self.services.app_service.line_bot_api.get_profile(
                user_id)
            return profile.display_name
        except Exception as err:
            target = self.services.app_service.db.session\
                .query(Users).filter(Users.user_id == user_id).first()
            return target.name

    def get_user_id_by_name(self, name):
        target = self.services.app_service.db.session\
            .query(Users).filter(Users.name == name).first()
        return target.user_id

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
            self.services.reply_service.add_message(
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
            self.services.reply_service.add_message(
                'ユーザーを認識できませんでした。お手数おかけしますが当アカウントを一度ブロックし、ブロック解除してください'
            )
            return
        return target.mode

    def reply_mode(self):
        self.services.reply_service.add_message(self.get_mode())

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

    def create(self, name, user_id):
        """create"""
        new_user = Users(
            name=name,
            user_id=user_id,
            mode=self.modes.wait.value,
        )
        self.services.app_service.db.session.add(new_user)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'create: {new_user.user_id} {new_user.name}')
        return new_user

    def set_zoom_id(self, zoom_id):
        user_id = self.services.app_service.req_user_id
        target = self.services.app_service.db.session\
            .query(Users).filter(Users.user_id == user_id).first()
        if target == None:
            self.services.app_service.logger.warning(f'set_zoom_url: user(id={user_id}) is not found')
            return
        target.zoom_id = zoom_id
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'set_user_url: {zoom_id} to {user_id}')
        self.services.reply_service.add_message(
            f'Zoom URL を登録しました。\nトークルームにて「_my_zoom」で呼び出すことができます。')

    def reply_zoom_id(self):
        user_id = self.services.app_service.req_user_id
        target = self.services.app_service.db.session\
            .query(Users).filter(Users.user_id == user_id).first()
        if target == None:
            self.services.app_service.logger.warning(f'reply_zoom_url: user(id={user_id}) is not found')
            return
        if target.zoom_id is None:
            self.services.reply_service.add_message(
                f'Zoom URL が登録されていません。個人チャットの設定から登録してください。')
            return
        self.services.reply_service.add_message(target.zoom_id)
        return
