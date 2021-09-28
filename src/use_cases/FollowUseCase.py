# flake8: noqa: E999
from server import line_bot_api
from services import (
    request_info_service,
    user_service,
    reply_service,
    rich_menu_service,
)


class FollowUseCase:

    def execute():
        """follow event"""
        profile = line_bot_api.get_profile(
            request_info_service.req_line_user_id
        )
        user = user_service.find_or_create_by_profile(profile)
        reply_service.add_message(
            f'こんにちは。\n麻雀対戦結果管理アカウントである Mahjong Manager は\
            {user.name}さんの快適な麻雀生活をサポートします。')
        rich_menu_service.create_and_link(
            request_info_service.req_line_user_id
        )
