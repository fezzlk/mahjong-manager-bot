"""router"""

from enum import Enum
import json


class UCommands(Enum):
    """UCommands"""

    exit = 'exit'
    mode = 'mode'
    payment = 'payment'
    analysis = 'analysis'
    fortune = 'fortune'
    history = 'history'
    help = 'help'
    setting = 'setting'
    github = 'github'
    users = 'users'
    d_users = 'd_users'
    d_rooms = 'd_rooms'
    d_results = 'd_results'
    d_matches = 'd_matches'
    d_configs = 'd_configs'
    test = 'test'


class RCommands(Enum):
    """RCommands"""

    start = 'start'
    exit = 'exit'
    input = 'input'
    mode = 'mode'
    help = 'help'
    calc = 'calculator'
    setting = 'setting'
    reset = 'reset'
    results = 'results'
    delete = 'delete'
    finish = 'finish'
    github = 'github'
    fortune = 'fortune'
    others = 'others'
    matches = 'matches'
    tobi = 'tobi'
    drop = 'drop'
    drop_m = 'drop_m'
    add_result = 'add_result'


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
        self.services.app_service.delete_req_info()

    def unfollow(self, event):
        """unfollow event"""
        self.services.app_service.set_req_info(event)
        self.services.user_service.delete(
            self.services.app_service.req_user_id
        )
        self.services.app_service.delete_req_info()

    def join(self, event):
        """join event"""

        self.services.app_service.set_req_info(event)
        self.services.reply_service.add_text(f'こんにちは、今日は麻雀日和ですね。')
        self.services.room_service.register()
        self.services.reply_service.reply(event)
        self.services.app_service.delete_req_info()

    def textMessage(self, event):
        """receive text message event"""
        self.services.app_service.set_req_info(event)
        if self.services.app_service.req_room_id != None:
            self.routing_in_room_by_text(event)
        else:
            self.routing_by_text(event)
        self.services.reply_service.reply(event)
        self.services.app_service.delete_req_info()

    def imageMessage(self, event):
        """receive image message event"""

        self.services.app_service.set_req_info(event)
        message_id = event.message.id
        # message_idから画像のバイナリデータを取得
        message_content = self.services.app_service.line_bot_api.get_message_content(
            message_id
        )

        path = f"images/results/{message_id}.jpg"
        with open(path, "wb") as f:
            # バイナリを1024バイトずつ書き込む
            for chunk in message_content.iter_content():
                f.write(chunk)

        self.services.points_service.add_by_ocr(path)
        self.services.reply_service.reply(event)
        self.services.app_service.delete_req_info()

    def postback(self, event):
        """postback event"""

        self.services.app_service.set_req_info(event)
        method = event.postback.data[1:]
        if self.services.app_service.req_room_id != None:
            self.routing_in_room_by_method(method)
        else:
            print(method)
            self.routing_by_method(method)
        self.services.reply_service.reply(event)
        self.services.app_service.delete_req_info()

    def routing_by_text(self, event):
        """routing by text for personal chat"""

        text = event.message.text
        prefix = text[0]
        if len(text) > 1:
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
        # payment
        elif method == UCommands.payment.name:
            self.services.reply_service.add_text('この機能は開発中です。')
        # analysis
        elif method == UCommands.analysis.name:
            self.services.reply_service.add_text('この機能は開発中です。')
        # fortune
        elif method == UCommands.fortune.name:
            self.services.reply_service.add_text(
                f'あなたの今日のラッキー牌は「{self.services.app_service.get_random_hai()}」です。')
        # history
        elif method == UCommands.history.name:
            self.services.reply_service.add_text('この機能は開発中です。')
        # setting
        elif method == UCommands.setting.name:
            self.services.reply_service.add_text('この機能は開発中です。')
        # help
        elif method == UCommands.help.name:
            self.services.reply_service.add_text('使い方は明日書きます。')
            self.services.reply_service.add_text(
                '\n'.join(['_' + e.name for e in UCommands]))
        # github
        elif method == UCommands.github.name:
            self.services.reply_service.add_text(
                'https://github.com/bbladr/mahjong-manager-bot')
        # users
        elif method == UCommands.users.name:
            self.services.user_service.reply_all()
        # dev users
        elif method == UCommands.d_users.name:
            self.services.user_service.reply_all_records()
        # dev rooms
        elif method == UCommands.d_rooms.name:
            self.services.room_service.reply_all_records()
        # dev results
        elif method == UCommands.d_results.name:
            self.services.results_service.reply_all_records()
        # dev matches
        elif method == UCommands.d_matches.name:
            self.services.matches_service.reply_all_records()
        # dev configs
        elif method == UCommands.d_configs.name:
            self.services.config_service.reply_all_records()
        # dev test
        elif method == UCommands.test.name:
            self.services.ocr_service.run_test()

    def routing_in_room_by_text(self, event):
        """routing by text"""
        self.services.room_service.register()

        text = event.message.text
        prefix = text[0]
        if len(text) > 1:
            if (prefix == '_') & (text[1:].split()[0] in [e.name for e in RCommands]):
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

        # start menu
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
            self.services.results_service.reset_points()
        # results
        elif method == RCommands.results.name:
            self.services.matches_service.reply_sum_results()
        # drop
        elif method.startswith(RCommands.drop.name):
            a = method.split()
            if len(a) < 2:
                return
            target_time = int(a[1])
            self.services.matches_service.drop_result_by_time(target_time)
        elif method == RCommands.drop_m.name:
            self.services.matches_service.drop_current()
        # delete
        elif method == RCommands.delete.name:
            self.services.room_service.chmod(
                services.room_service.modes.delete)
        # finish
        elif method == RCommands.finish.name:
            self.services.matches_service.finish()
        # github
        elif method == RCommands.github.name:
            self.services.reply_service.add_text(
                'https://github.com/bbladr/mahjong-manager-bot')
        # fortune
        elif method == RCommands.fortune.name:
            self.services.reply_service.add_text(
                f'あなたの今日のラッキー牌は「{self.services.app_service.get_random_hai()}」です。')
        # others manu
        elif method == RCommands.others.name:
            self.services.reply_service.add_others_menu()
        # matches
        elif method == RCommands.matches.name:
            self.services.matches_service.reply()
        elif method.startswith(RCommands.tobi.name):
            tobashita_player = method[5:]
            self.services.calculate_service.calculate(
                tobashita_player=tobashita_player)
        # add results
        elif method.startswith(RCommands.add_result.name):
            results = method[11:]
            self.services.results_service.add()
            self.services.calculate_service.calculate(
                json.loads(results)
            )
