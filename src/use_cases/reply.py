# flake8: noqa: E999
from services import (
    request_info_service,
    reply_service,
    message_service,
    user_service,
)


class ReplyUseCases:
    """reply use cases"""

    def add_start_menu(self):
        reply_service.add_start_menu()

    def add_others_menu(self):
        reply_service.add_others_menu()

    def reply_fortune(self):
        line_id = request_info_service.req_line_user_id
        reply_service.add_message(
            f'{user_service.get_name_by_line_user_id(line_id)}さんの今日のラッキー牌は「{message_service.get_random_hai(line_id)}」です。'
        )

    def reply_user_help(self, UCommands):
        reply_service.add_message('使い方は明日書きます。')
        reply_service.add_message(
            '\n'.join(['_' + e.name for e in UCommands])
        )

    def reply_room_help(self, RCommands):
        reply_service.add_message('使い方は明日書きます。')
        reply_service.add_message(
            '\n'.join(['_' + e.name for e in RCommands]))

    def reply_github_url(self):
        reply_service.add_message(
            'https://github.com/bbladr/mahjong-manager-bot'
        )
