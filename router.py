"""router"""

from enum import Enum


class Commands(Enum):
    """Commands"""

    start = 'start'
    exit = 'exit'
    input = 'input'
    mode = 'mode'
    help = 'help'
    calc = 'calculator'
    setting = 'settings'
    off = 'off'
    on = 'on'
    reset = 'reset'
    results = 'results'
    delete = 'delete'
    finish = 'finish'
    github = 'github'
    register = 'register'


class Router:
    """router"""

    def __init__(self, services):
        self.services = services

    def follow(self, event):
        """follow event"""

        self.set_req_info(event)
        self.services.app_service.req_user_id = event.source.user_id
        profile = self.services.app_service.line_bot_api.get_profile(
            self.services.app_service.req_user_id)
        self.services.user_service.register(profile)

        self.services.reply_service.add_text(
            f'こんにちは。\n麻雀対戦結果自動管理アカウントである Mahjong Manager は\
            {profile.display_name}さんの快適な麻雀生活をサポートします。')
        self.services.reply_service.reply(event)
        self.services.rich_menu_service.create_and_link('personal')

    def join(self, event):
        """join event"""

        self.set_req_info(event)
        self.services.reply_service.add_text(f'こんにちは、今日は麻雀日和ですね。')
        self.services.room_service.register()
        self.services.reply_service.reply(event)

    def textMessage(self, event):
        """receive text message event"""

        set_req_info(event)
        routing_by_text(event)
        self.services.reply_service.reply(event)

    def imageMessage(self, event):
        """receive image message event"""

        set_req_info(event)
        self.services.reply_service.add_text(
            '画像への返信はまだサポートされていません。開発者に寄付をすれば対応を急ぎます。')
        self.services.reply_service.reply(event)

    def postback(self, event):
        """postback event"""

        set_req_info(event)
        method = event.postback.data[1:]
        routing_by_method(method)
        self.services.reply_service.reply(event)

    def set_req_info(self, event):
        """set request info"""

        self.services.app_service.req_user_id = event.source.user_id
        if event.source.type == 'room':
            services.app_service.req_room_id = event.source.room_id

    def routing_by_text(self, event):
        """routing by text"""

        text = event.message.text
        prefix = text[0]
        if (prefix == '_') & (text[1:] in [e.name for e in Commands]):
            routing_by_method(text[1:])
            return

        # routing by mode
        # inpuy mode
        if self.services.room_service.get_mode() == self.services.room_service.modes.input:
            self.services.points_service.add_by_text(text)
            return

        # delete mode
        if self.services.room_service.get_mode() == self.services.room_service.modes.delete:
            self.services.results_service.delete_by_text(text)
            return

        # off mode
        if self.services.room_service.get_mode() == self.services.room_service.modes.input:
            return

        # wait mode
        if prefix == '_':
            self.services.reply_service.add_text(
                '使い方がわからない場合はメニューの中の「使い方」を押してください。')
            return
        self.services.reply_service.add_text('雑談してる暇があったら麻雀の勉強をしましょう')

    def routing_by_method(self, method):
        """routing by method"""

        # start
        if method == Commands.start.name:
            self.services.reply_service.add_start_menu()
        # register
        if method == Commands.register.name:
            self.services.room_service.register()
        # input
        if method == Commands.input.name:
            self.services.points_service.reset()
            self.services.room_service.chmod(services.room_service.modes.input)
        # calculate
        elif method == Commands.calc.name:
            self.services.calculate_service.calculate()
        # mode
        elif method == Commands.mode.name:
            self.services.room_service.reply_mode()
        # exit
        elif method == Commands.exit.name:
            self.services.room_service.chmod(services.room_service.modes.wait)
        # help
        elif method == Commands.help.name:
            self.services.reply_service.add_text('使い方は明日書きます。')
            self.services.reply_service.add_text(
                '\n'.join(['_' + e.name for e in Commands]))
        # setting
        elif method == Commands.setting.name:
            self.services.config_service.reply()
        # off
        elif method == Commands.off.name:
            self.services.room_service.chmod(services.room_service.modes.off)
        # on
        elif method == Commands.on.name:
            self.services.room_service.chmod(services.room_service.modes.wait)
        # reset
        elif method == Commands.reset.name:
            self.services.results_service.reset()
        # results
        elif method == Commands.results.name:
            self.services.results_service.reply_all()
        # delete
        elif method == Commands.delete.name:
            self.services.room_service.chmod(
                services.room_service.modes.delete)
        # finish
        elif method == Commands.finish.name:
            self.services.results_service.finish()
        # github
        elif method == Commands.github.name:
            self.services.reply_service.add_text(
                'https://github.com/bbladr/mahjong-manager-bot')
