"""router"""

from enum import Enum
import json

from server import logger, line_bot_api
from services import (
    app_service,
    reply_service,
    rich_menu_service,
    ocr_service,
    message_service,
)
from use_cases import (
    user_use_cases,
    room_use_cases,
    points_use_cases,
    calculate_use_cases,
    config_use_cases,
    matches_use_cases,
    hanchans_use_cases,
)


class UCommands(Enum):
    """Commands for personal user"""

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
    """Commands for room"""

    start = 'start'
    exit = 'exit'
    input = 'input'
    mode = 'mode'
    help = 'help'
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
    """router(TODO: abolish Router class)"""

    def root(self, event):
        """root"""
        logger.info(f'receive {event.type} event')
        app_service.set_req_info(event)
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
            logger.exception(err)
            reply_service.add_message(str(err))

        if isEnabledReply:
            reply_service.reply(event)
        app_service.delete_req_info()

    def follow(self, event):
        """follow event"""
        user = user_use_cases.register()
        reply_service.add_message(
            f'こんにちは。\n麻雀対戦結果自動管理アカウントである Mahjong Manager は\
            {user.name}さんの快適な麻雀生活をサポートします。')
        rich_menu_service.create_and_link(app_service.req_user_id)

    def unfollow(self, event):
        """unfollow event"""
        user_use_cases.delete_by_user_id(
            app_service.req_user_id
        )

    def join(self, event):
        """join event"""
        reply_service.add_message(
            'こんにちは、今日は麻雀日和ですね。'
        )
        room_use_cases.register()

    def textMessage(self, event):
        """receive text message event"""
        user_use_cases.register()
        if event.source.type == 'room':
            self.routing_for_room_by_text(event)
        elif event.source.type == 'user':
            self.routing_by_text(event)
        else:
            logger.info(
                f'message.source.type: {event.source.type}'
            )
            raise BaseException('this sender is not supported')

    def imageMessage(self, event):
        """receive image message event"""
        if event.source.type == 'room':
            message_content = line_bot_api.get_message_content(
                event.message.id
            )
            ocr_service.run(message_content.content)
            if ocr_service.isResultImage():
                points_use_cases.add_by_ocr()
            else:
                logger.warning(
                    'this image is not result of jantama'
                )
            ocr_service.delete_result()

    def postback(self, event):
        """postback event"""

        text = event.postback.data
        method = text[1:].split()[0]
        body = text[len(method) + 2:]
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
                body = text[len(method) + 2:]
                self.routing_by_method(method, body)
                return
            else:
                reply_service.add_message(
                    '使い方がわからない場合はメニューの中の「使い方」を押してください。'
                )
                return

        """routing by text on each mode"""
        """wait mode"""
        reply_service.add_message(
            message_service.get_wait_massage(app_service.req_user_id))

        """if zoom url, register to room"""
        if '.zoom.us' in text:
            user_use_cases.set_zoom_id(text)

    def routing_by_method(self, method, body):
        """routing by method for personal chat"""

        # mode
        if method == UCommands.mode.name:
            user_use_cases.reply_mode()
        # exit
        elif method == UCommands.exit.name:
            user_use_cases.chmod(
                user_use_cases.modes.wait
            )
        # payment
        elif method == UCommands.payment.name:
            reply_service.add_message('支払い機能は開発中です。')
        # analysis
        elif method == UCommands.analysis.name:
            reply_service.add_message('分析機能は開発中です。')
        # fortune
        elif method == UCommands.fortune.name:
            reply_service.add_message(
                f'あなたの今日のラッキー牌は「{message_service.get_random_hai(app_service.req_user_id)}」です。'
            )
        # history
        elif method == UCommands.history.name:
            reply_service.add_message('対戦履歴機能は開発中です。')
        # setting
        elif method == UCommands.setting.name:
            reply_service.add_message('個人設定機能は開発中です。')
        # help
        elif method == UCommands.help.name:
            reply_service.add_message('使い方は明日書きます。')
            reply_service.add_message(
                '\n'.join(['_' + e.name for e in UCommands])
            )
        # github
        elif method == UCommands.github.name:
            reply_service.add_message(
                'https://github.com/bbladr/mahjong-manager-bot'
            )

    def routing_for_room_by_text(self, event):
        """routing by text"""
        user_use_cases.register()

        text = event.message.text
        if (text[0] == '_') & (len(text) > 1):
            method = text[1:].split()[0]
            if method in [c.name for c in RCommands]:
                body = text[len(method) + 2:]
                self.routing_for_room_by_method(method, body)
                return
            else:
                reply_service.add_message(
                    '使い方がわからない場合は「_help」と入力してください。'
                )
                return

        """routing by text on each mode"""
        current_mode = room_use_cases.get_mode()
        """input mode"""
        if current_mode == room_use_cases.modes.input.value:
            points_use_cases.add_by_text(text)
            return

        """wait mode"""
        """if text is result, add result"""
        rows = [r for r in text.split('\n') if ':' in r]
        if len(rows) == 4:
            points = {}
            for r in rows:
                col = r.split(':')
                points[
                    user_use_cases.get_user_id_by_name(col[0])
                ] = int(col[1])
            hanchans_use_cases.add(points)
            calculate_use_cases.calculate(
                points
            )

        """if zoom url, register to room"""
        if '.zoom.us' in text:
            room_use_cases.set_zoom_url(text)

    def routing_for_room_by_method(self, method, body):
        """routing by method"""
        # start menu
        if method == RCommands.start.name:
            reply_service.add_start_menu()
        # input
        elif method == RCommands.input.name:
            hanchans_use_cases.add()
            room_use_cases.chmod(
                room_use_cases.modes.input
            )
        # mode
        elif method == RCommands.mode.name:
            mode = room_use_cases.get_mode()
            reply_service.add_message(mode)
        # exit
        elif method == RCommands.exit.name:
            room_use_cases.chmod(
                room_use_cases.modes.wait
            )
        # help
        elif method == RCommands.help.name:
            reply_service.add_message('使い方は明日書きます。')
            reply_service.add_message(
                '\n'.join(['_' + e.name for e in RCommands]))
        # setting
        elif method == RCommands.setting.name:
            config_use_cases.reply()
            reply_service.add_settings_menu(body)
        # reset
        elif method == RCommands.reset.name:
            room_use_cases.reset_points()
        # results
        elif method == RCommands.results.name:
            room_use_cases.reply_sum_results()
        # results by match id
        elif method == RCommands.match.name:
            matches_use_cases.reply_sum_results(body)
        # drop
        elif method == RCommands.drop.name:
            matches_use_cases.drop_result_by_number(int(body))
        # drop match
        elif method == RCommands.drop_m.name:
            matches_use_cases.disable()
        # finish
        elif method == RCommands.finish.name:
            matches_use_cases.finish()
        # fortune
        elif method == RCommands.fortune.name:
            reply_service.add_message(
                f'{user_use_cases.get_name_by_user_id()}さんの今日のラッキー牌は「{message_service.get_random_hai(app_service.req_user_id)}」です。'
            )
        # others menu
        elif method == RCommands.others.name:
            reply_service.add_others_menu()
        # matches
        elif method == RCommands.matches.name:
            matches_use_cases.reply()
        # tobi
        elif method == RCommands.tobi.name:
            calculate_use_cases.calculate(
                tobashita_player_id=body)
        # add results
        elif method == RCommands.add_result.name:
            points = json.loads(body)
            hanchans_use_cases.add(points)
            calculate_use_cases.calculate(
                points
            )
        # update config
        elif method == RCommands.update_config.name:
            key = body.split(' ')[0]
            value = body.split(' ')[1]
            config_use_cases.update(
                key, value
            )
        # zoom
        elif method == RCommands.zoom.name:
            room_use_cases.reply_zoom_url()
        # my_zoom
        elif method == RCommands.my_zoom.name:
            user_use_cases.reply_zoom_id()
            room_use_cases.set_zoom_url(body)
        # sum_matches
        elif method == RCommands.sum_matches.name:
            args = body.split(' ')
            while 'to' in args:
                index = args.index('to')
                if index != 0 and len(args) - 1 > index:
                    args += [
                        str(i) for i in range(
                            int(args[index - 1]),
                            int(args[index + 1]) + 1
                        )
                    ]
                args.remove('to')
            matches_use_cases.reply_sum_matches_by_ids(args)
        # graphs
        elif method == RCommands.graph.name:
            matches_use_cases.plot()


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
