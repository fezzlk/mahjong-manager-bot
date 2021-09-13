# flake8: noqa: E999
"""user"""

from enum import Enum
from server import line_bot_api
from services import (
    app_service,
    user_service,
    reply_service,
    rich_menu_service,
)


class Modes(Enum):
    """mode"""

    wait = 'wait'


class UserUseCases:
    """user use cases"""

    def __init__(self):
        self.modes = Modes

    def get(self):
        """web"""
        user_service.get()

    def create(self, name, user_id):
        """web"""
        user_service.create(name, user_id)

    def delete(self, ids):
        """web"""
        user_service.delete(ids)

    def follow(self):
        """follow event"""
        profile = line_bot_api.get_profile(
            app_service.req_user_line_id
        )
        user = user_service.find_or_create_by_profile(profile)
        reply_service.add_message(
            f'こんにちは。\n麻雀対戦結果自動管理アカウントである Mahjong Manager は\
            {user.name}さんの快適な麻雀生活をサポートします。')
        rich_menu_service.create_and_link(app_service.req_user_line_id)

    def unfollow(self):
        """unfollow event"""
        user_service.delete_by_user_id(
            app_service.req_user_line_id
        )

    def reply_mode(self):
        user_id = app_service.req_user_line_id
        mode = user_service.get_mode(user_id)
        if mode is None:
            reply_service.add_message(
                'ユーザーを認識できませんでした。当アカウントを一度ブロックし、ブロック解除してください。'
            )
            return
        reply_service.add_message(mode)

    def chmod(self, user_id, mode):
        user_service.chmod(user_id, mode)

    def set_zoom_id(self, zoom_id):
        user_id = app_service.req_user_line_id
        result = user_service(user_id, zoom_id)

        if result is None:
            self.services.reply_service.add_message(
                'Zoom URL の登録に失敗しました。')
            return

        self.services.reply_service.add_message(
            'Zoom URL を登録しました。\nトークルームにて「_my_zoom」で呼び出すことができます。')

    def reply_zoom_id(self):
        user_id = app_service.req_user_line_id
        zoom_id = user_service.get_zoom_id(user_id)
        if zoom_id is None:
            self.services.reply_service.add_message(
                'Zoom URL を取得できませんでした。')
            return
        self.services.reply_service.add_message(zoom_id)
