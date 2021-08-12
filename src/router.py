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
    finish = 'finish'
    fortune = 'fortune'
    others = 'others'
    matches = 'matches'
    match = 'match'
    tobi = 'tobi'
    drop = 'drop'
    drop_m = 'drop_m'
    add_result = 'add_result'
    update_config = 'update_config'
    zoom = 'zoom'
    my_zoom = 'my_zoom'
    sum_matches = 'sum_matches'
    graph = 'graph'


class Router:
    """router"""

    def __init__(self, services):
        self.services = services

    def root(self, event):
        """root"""
        self.services.app_service.logger.info(f'receive {event.type} event')
        self.services.app_service.set_req_info(event)
        isEnabledReply = True
        try:
            if event.type == 'message':
                if event.message.type == 'text':
                    self.textMessage(event)
                elif event.message.type == 'image':
                    self.imageMessage(event)
            elif event.type == 'follow':
                self.follow(event)
            elif event.type == 'unfollow':
                self.unfollow(event)
                isEnabledReply = False
            elif event.type == 'join':
                self.join(event)
            elif event.type == 'postback':
                self.postback(event)
        except BaseException as err:
            self.services.app_service.logger.exception(err)
            self.services.reply_service.add_message(str(err))

        if isEnabledReply == True:
            self.services.reply_service.reply(event)
        self.services.app_service.delete_req_info()

    def follow(self, event):
        """follow event"""
        user = self.services.user_service.register()
        self.services.reply_service.add_message(
            f'こんにちは。\n麻雀対戦結果自動管理アカウントである Mahjong Manager は\
            {user.name}さんの快適な麻雀生活をサポートします。')
        self.services.rich_menu_service.create_and_link()

    def unfollow(self, event):
        """unfollow event"""
        self.services.user_service.delete_by_user_id(
            self.services.app_service.req_user_id
        )

    def join(self, event):
        """join event"""
        self.services.reply_service.add_message(f'こんにちは、今日は麻雀日和ですね。')
        self.services.room_service.register()

    def textMessage(self, event):
        """receive text message event"""
        self.services.user_service.register()
        if event.source.type == 'room':
            self.routing_for_room_by_text(event)
        elif event.source.type == 'user':
            self.routing_by_text(event)
        else:
            self.services.app_service.logger.info(f'message.source.type: {event.source.type}')
            raise BaseException('this sender is not supported')

    def imageMessage(self, event):
        """receive image message event"""
        if event.source.type == 'room':
            message_content = self.services.app_service.line_bot_api.get_message_content(
                event.message.id
            )
            self.services.ocr_service.run(message_content.content)
            if self.services.ocr_service.isResultImage():
                self.services.points_service.add_by_ocr()
            else:
                self.services.app_service.logger.warning(
                    'this image is not result of jantama'
                )
            self.services.ocr_service.delete_result()

    def postback(self, event):
        """postback event"""

        text = event.postback.data
        method = text[1:].split()[0]
        body = text[len(method)+2:]
        if event.source.type == 'room':
            self.routing_for_room_by_method(method, body)
        elif event.source.type == 'user':
            self.routing_by_method(method, body)

    def routing_by_text(self, event):
        """routing by text for personal chat"""
        text = event.message.text
        if (text[0] == '_') & (len(text) > 1):
            method = text[1:].split()[0]
            if method in [c.name for c in UCommands]:
                body = text[len(method)+2:]
                self.routing_by_method(method, body)
                return
            else:
                self.services.reply_service.add_message(
                    '使い方がわからない場合はメニューの中の「使い方」を押してください。'
                )
                return

        """routing by text on each mode"""
        """wait mode"""
        self.services.reply_service.add_message(
            self.services.message_service.get_wait_massage())

        """if zoom url, register to room"""
        if '.zoom.us' in text:
            self.services.user_service.set_zoom_id(text)

    def routing_by_method(self, method, body):
        """routing by method for personal chat"""

        # mode
        if method == UCommands.mode.name:
            self.services.user_service.reply_mode()
        # exit
        elif method == UCommands.exit.name:
            self.services.user_service.chmod(
                self.services.user_service.modes.wait
            )
        # payment
        elif method == UCommands.payment.name:
            self.services.reply_service.add_message('支払い機能は開発中です。')
        # analysis
        elif method == UCommands.analysis.name:
            self.services.reply_service.add_message('分析機能は開発中です。')
        # fortune
        elif method == UCommands.fortune.name:
            self.services.reply_service.add_message(
                f'あなたの今日のラッキー牌は「{self.services.message_service.get_random_hai()}」です。')
        # history
        elif method == UCommands.history.name:
            self.services.reply_service.add_message('対戦履歴機能は開発中です。')
        # setting
        elif method == UCommands.setting.name:
            self.services.reply_service.add_message('個人設定機能は開発中です。')
        # help
        elif method == UCommands.help.name:
            self.services.reply_service.add_message('使い方は明日書きます。')
            self.services.reply_service.add_message(
                '\n'.join(['_' + e.name for e in UCommands])
            )
        # github
        elif method == UCommands.github.name:
            self.services.reply_service.add_message(
                'https://github.com/bbladr/mahjong-manager-bot'
            )

    def routing_for_room_by_text(self, event):
        """routing by text"""
        self.services.room_service.register()

        text = event.message.text
        if (text[0] == '_') & (len(text) > 1):
            method = text[1:].split()[0]
            if method in [c.name for c in RCommands]:
                body = text[len(method)+2:]
                self.routing_for_room_by_method(method, body)
                return
            else:
                self.services.reply_service.add_message(
                    '使い方がわからない場合は「_help」と入力してください。'
                )
                return

        """routing by text on each mode"""
        current_mode = self.services.room_service.get_mode()
        """input mode"""
        if current_mode == self.services.room_service.modes.input.value:
            self.services.points_service.add_by_text(text)
            return

        """wait mode"""
        """if text is result, add result"""
        rows = [r for r in text.split('\n') if ':' in r]
        if len(rows) == 4:
            points = {}
            for r in rows:
                col = r.split(':')
                points[
                    self.services.user_service.get_user_id_by_name(col[0])
                ] = int(col[1])
            self.services.results_service.add(points)
            self.services.calculate_service.calculate(
                points
            )

        """if zoom url, register to room"""
        if '.zoom.us' in text:
            self.services.room_service.set_zoom_url(text)

    def routing_for_room_by_method(self, method, body):
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
            self.services.reply_service.add_message(mode)
        # exit
        elif method == RCommands.exit.name:
            self.services.room_service.chmod(
                self.services.room_service.modes.wait
            )
        # help
        elif method == RCommands.help.name:
            self.services.reply_service.add_message('使い方は明日書きます。')
            self.services.reply_service.add_message(
                '\n'.join(['_' + e.name for e in RCommands]))
        # setting
        elif method == RCommands.setting.name:
            self.services.reply_service.add_settings_menu(body)
        # reset
        elif method == RCommands.reset.name:
            self.services.results_service.reset_points()
        # results
        elif method == RCommands.results.name:
            self.services.matches_service.reply_sum_results()
        # results by match id
        elif method == RCommands.match.name:
            self.services.matches_service.reply_sum_results(body)
        # drop
        elif method == RCommands.drop.name:
            self.services.matches_service.drop_result_by_number(int(body))
        # drop match
        elif method == RCommands.drop_m.name:
            self.services.matches_service.disable()
        # finish
        elif method == RCommands.finish.name:
            self.services.matches_service.finish()
        # fortune
        elif method == RCommands.fortune.name:
            self.services.reply_service.add_message(
                f'{self.services.user_service.get_name_by_user_id()}さんの今日のラッキー牌は「{self.services.message_service.get_random_hai()}」です。')
        # others menu
        elif method == RCommands.others.name:
            self.services.reply_service.add_others_menu()
        # matches
        elif method == RCommands.matches.name:
            self.services.matches_service.reply()
        # tobi
        elif method == RCommands.tobi.name:
            self.services.calculate_service.calculate(
                tobashita_player_id=body)
        # add results
        elif method == RCommands.add_result.name:
            points = json.loads(body)
            self.services.results_service.add(points)
            self.services.calculate_service.calculate(
                points
            )
        # update config
        elif method == RCommands.update_config.name:
            key = body.split(' ')[0]
            value = body.split(' ')[1]
            self.services.config_service.update(
                key, value
            )
        # zoom
        elif method == RCommands.zoom.name:
            self.services.room_service.reply_zoom_url()
        # my_zoom
        elif method == RCommands.my_zoom.name:
            self.services.user_service.reply_zoom_id()
            self.services.room_service.set_zoom_url(body)
        # sum_matches
        elif method == RCommands.sum_matches.name:
            args = body.split(' ')
            month = None
            while 'to' in args:
                index = args.index('to')
                if index != 0 and len(args)-1 > index:
                    args += [
                        str(i) for i in range(int(args[index-1]), int(args[index+1])+1)
                    ]
                args.remove('to')
            self.services.matches_service.reply_sum_matches_by_ids(args)
        # graphes
        elif method == RCommands.graph.name:
            self.services.matches_service.plot()


# def parse_int_list(args):
#     args = body.split(' ')
#     month = None
#     while 'to' in args:
#         index = args.index('to')
#         if index != 0 and len(args)-1 > index:
#             args += [
#                 str(i) for i in range(args[index-1], args[index+1]+1)
#             ]
#         args.remove('to')
