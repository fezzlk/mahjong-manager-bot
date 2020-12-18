"""router"""

from enum import Enum


class UCommands(Enum):
    """UCommands"""

    exit = 'exit'
    mode = 'mode'
    help = 'help'
    github = 'github'


class RCommands(Enum):
    """RCommands"""

    start = 'start'
    exit = 'exit'
    input = 'input'
    mode = 'mode'
    help = 'help'
    calc = 'calculator'
    setting = 'settings'
    reset = 'reset'
    results = 'results'
    delete = 'delete'
    finish = 'finish'
    github = 'github'
    recommend = 'recommend'
    others = 'others'


class Router:
    """router"""

    def __init__(self, services):
        self.services = services

    def follow(self, event):
        """follow event"""

        self.services.app_service.set_req_info(event)
        profile = self.services.app_service.line_bot_api.get_profile(
            self.services.app_service.req_user_id)
        self.services.user_service.register(profile)

        self.services.reply_service.add_text(
            f'こんにちは。\n麻雀対戦結果自動管理アカウントである Mahjong Manager は\
            {profile.display_name}さんの快適な麻雀生活をサポートします。')
        self.services.reply_service.reply(event)
        self.services.rich_menu_service.create_and_link('personal')

    def unfollow(self, event):
        """unfollow event"""
        self.services.app_service.set_req_info(event)
        self.services.user_service.delete(
            self.services.app_service.req_user_id
        )

    def join(self, event):
        """join event"""

        self.services.app_service.set_req_info(event)
        self.services.reply_service.add_text(f'こんにちは、今日は麻雀日和ですね。')
        self.services.room_service.register()
        self.services.reply_service.reply(event)

    def textMessage(self, event):
        """receive text message event"""
        self.services.app_service.set_req_info(event)
        if self.services.app_service.req_room_id != None:
            self.routing_in_room_by_text(event)
        else:
            self.routing_by_text(event)
        self.services.reply_service.reply(event)

    def imageMessage(self, event):
        """receive image message event"""

        self.services.app_service.set_req_info(event)
        self.services.reply_service.add_text(
            '画像への返信はまだサポートされていません。開発者にお金を寄付すれば対応を急ぎます。')
        self.services.reply_service.reply(event)

    def postback(self, event):
        """postback event"""

        self.services.app_service.set_req_info(event)
        method = event.postback.data[1:]
        if self.services.app_service.req_room_id != None:
            self.routing_in_room_by_method(method)
        else:
            self.routing_by_method(method)
        self.services.reply_service.reply(event)

    def routing_by_text(self, event):
        """routing by text for personal chat"""

        text = event.message.text
        prefix = text[0]
        if (prefix == '_') & (text[1:] in [e.name for e in UCommands]):
            self.routing_by_method(text[1:])
            return

        # routing by mode
        # wait mode
        if prefix == '_':
            self.services.reply_service.add_text(
                '使い方がわからない場合はメニューの中の「使い方」を押してください。')
            return
        # the other
        self.services.reply_service.add_text('雑談してる暇があったら麻雀の勉強をしましょう')

    def routing_by_method(self, method):
        """routing by method for personal chat"""

        # mode
        if method == UCommands.mode.name:
            mode = self.services.user_service.get_mode()
            self.services.reply_service.add_text(mode)
        # exit
        elif method == UCommands.exit.name:
            self.services.user_service.chmod(
                self.services.user_service.modes.wait
            )
        # help
        elif method == UCommands.help.name:
            self.services.reply_service.add_text('使い方は明日書きます。')
            self.services.reply_service.add_text(
                '\n'.join(['_' + e.name for e in UCommands]))
        # github
        elif method == UCommands.github.name:
            self.services.reply_service.add_text(
                'https://github.com/bbladr/mahjong-manager-bot')

    def routing_in_room_by_text(self, event):
        """routing by text"""
        self.services.room_service.register()

        text = event.message.text
        prefix = text[0]
        if (prefix == '_') & (text[1:] in [e.name for e in RCommands]):
            self.routing_in_room_by_method(text[1:])
            return

        current_mode = self.services.room_service.get_mode()
        # routing by mode
        # input mode
        if current_mode == self.services.room_service.modes.input.value:
            self.services.points_service.add_by_text(text)
            return

        # delete mode
        if current_mode == self.services.room_service.modes.delete.value:
            self.services.results_service.delete_by_text(text)
            return

        # wait mode
        if prefix == '_':
            self.services.reply_service.add_text(
                '使い方がわからない場合はメニューの中の「使い方」を押してください。')
            return

    def routing_in_room_by_method(self, method):
        """routing by method"""

        # start
        if method == RCommands.start.name:
            self.services.reply_service.add_start_menu()
        # input
        elif method == RCommands.input.name:
            self.services.results_service.add()
            self.services.room_service.chmod(
                self.services.room_service.modes.input
            )
        # calculate
        elif method == RCommands.calc.name:
            self.services.calculate_service.calculate()
        # mode
        elif method == RCommands.mode.name:
            mode = self.services.room_service.get_mode()
            self.services.reply_service.add_text(mode)
        # exit
        elif method == RCommands.exit.name:
            self.services.room_service.chmod(
                self.services.room_service.modes.wait
            )
        # help
        elif method == RCommands.help.name:
            self.services.reply_service.add_text('使い方は明日書きます。')
            self.services.reply_service.add_text(
                '\n'.join(['_' + e.name for e in RCommands]))
        # setting
        elif method == RCommands.setting.name:
            self.services.config_service.reply()
            self.services.reply_service.add_settings_menu()
        # reset
        elif method == RCommands.reset.name:
            self.services.results_service.reset()
        # results
        elif method == RCommands.results.name:
            self.services.results_service.reply_all()
        # delete
        elif method == RCommands.delete.name:
            self.services.room_service.chmod(
                services.room_service.modes.delete)
        # finish
        elif method == RCommands.finish.name:
            self.services.reply_service.add_text(
                'この機能はまだ使えません。開発者にお金を寄付すれば対応を急ぎます。')
            # self.services.results_service.finish()
        # github
        elif method == RCommands.github.name:
            self.services.reply_service.add_text(
                'https://github.com/bbladr/mahjong-manager-bot')
        elif method == RCommands.recommend.name:
            self.services.reply_service.add_text(
                f'あなたの今日のラッキー牌は「{self.services.app_service.get_random_hai()}」です。')
        elif method == RCommands.others.name:
            self.services.reply_service.add_others_menu()
