"""router"""

from enum import Enum
import json

from server import logger, line_bot_api
from services import (
    app_service,
    reply_service,
    message_service,
    room_service,
)
from use_cases import (
    user_use_cases,
    room_use_cases,
    points_use_cases,
    calculate_use_cases,
    config_use_cases,
    ocr_use_cases,
    matches_use_cases,
    hanchans_use_cases,
    reply_use_case,
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
                user_use_cases.follow()
            elif event.type == 'unfollow':
                user_use_cases.unfollow()
                isEnabledReply = False
            elif event.type == 'join':
                room_use_cases.join()
            elif event.type == 'postback':
                self.postback(event)

        except BaseException as err:
            logger.exception(err)
            reply_service.add_message(str(err))

        if isEnabledReply:
            reply_service.reply(event)
        app_service.delete_req_info()

    def textMessage(self, event):
        """receive text message event"""
        if event.source.type == 'room':
            self.routing_for_room_by_text(event)
        elif event.source.type == 'user':
            self.routing_by_text(event)
        else:
            logger.info(
                f'error: message.source.type: {event.source.type}'
            )
            raise BaseException('this sender is not supported')

    def imageMessage(self, event):
        """receive image message event"""
        if event.source.type == 'room':
            message_content = line_bot_api.get_message_content(
                event.message.id
            )
            ocr_use_cases.input_result_from_image(message_content.content)

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
            message_service.get_wait_massage(app_service.req_user_line_id))

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
                app_service.req_user_line_id,
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
            reply_use_case.reply_fortune()
        # history
        elif method == UCommands.history.name:
            reply_service.add_message('対戦履歴機能は開発中です。')
        # setting
        elif method == UCommands.setting.name:
            reply_service.add_message('個人設定機能は開発中です。')
        # help
        elif method == UCommands.help.name:
            reply_use_case.reply_user_help(UCommands)
        # github
        elif method == UCommands.github.name:
            reply_use_case.reply_github_url()

    def routing_for_room_by_text(self, event):
        """routing by text"""
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
        room_id = app_service.req_room_id
        current_mode = room_service.get_mode(room_id)
        """input mode"""
        if current_mode == room_service.modes.input.value:
            points_use_cases.add_by_text(text)
            return

        """wait mode"""
        """if text is result, add result"""

        rows = [r for r in text.split('\n') if ':' in r]
        if len(rows) == 4:
            hanchans_use_cases.create_and_calculate_from_text_rows(rows)

        """if zoom url, register to room"""
        if '.zoom.us' in text:
            room_use_cases.set_zoom_url(text)

    def routing_for_room_by_method(self, method, body):
        """routing by method"""
        # start menu
        if method == RCommands.start.name:
            reply_use_case.add_start_menu()
        # input
        elif method == RCommands.input.name:
            room_use_cases.input_mode()
        # mode
        elif method == RCommands.mode.name:
            room_use_cases.reply_mode()
        # exit
        elif method == RCommands.exit.name:
            room_use_cases.wait_mode()
        # help
        elif method == RCommands.help.name:
            reply_use_case.reply_room_help()
        # setting
        elif method == RCommands.setting.name:
            config_use_cases.reply_menu(body)
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
            reply_use_case.reply_fortune()
        # others menu
        elif method == RCommands.others.name:
            reply_use_case.add_others_menu()
        # matches
        elif method == RCommands.matches.name:
            matches_use_cases.reply()
        # tobi
        elif method == RCommands.tobi.name:
            calculate_use_cases.calculate(
                tobashita_player_id=body)
        # add results
        elif method == RCommands.add_result.name:
            hanchans_use_cases.add_points(json.loads(body))
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
        # # graphs
        # elif method == RCommands.graph.name:
        #     matches_use_cases.plot()


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
