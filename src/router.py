from enum import Enum

from linebot.models.events import Event

from messaging_api_setting import line_bot_api
from services import (
    request_info_service,
    reply_service,
    message_service,
    group_service,
)
from use_cases import (
    follow_use_case,
    unfollow_use_case,
    join_group_use_case,
    add_point_by_text_use_case,
    add_hanchan_by_points_text_use_case,
    add_point_by_Json_text_use_case,
    start_input_use_case,
    group_quit_use_case,
    match_finish_use_case,
    reply_user_mode_use_case,
    reply_group_mode_use_case,
    user_exit_command_use_case,
    reply_fortune_use_case,
    reply_sum_hanchans_use_case,
    reply_matches_use_case,
    reply_user_help_use_case,
    reply_group_help_use_case,
    set_my_zoom_url_to_group_use_case,
    reply_github_url_use_case,
    reply_group_settings_menu_use_case,
    reply_others_menu_use_case,
    reply_start_menu_use_case,
    reply_sum_matches_by_ids_use_case,
    reply_sum_hanchans__by_match_id_use_case,
    set_zoom_url_to_user_use_case,
    set_zoom_url_to_group_use_case,
    calculate_with_tobi_use_case,
    update_config_use_case,
    input_result_from_image_use_case,
    reply_group_zoom_url_use_case,
    drop_hanchan_by_index_use_case,
    disable_match_use_case,
    user_my_zoom_command_use_case,
    reply_my_results_use_case,
)
from domains.Group import GroupMode


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
    my_zoom = 'my_zoom'


class RCommands(Enum):
    """Commands for group"""

    start = 'start'
    exit = 'exit'  # danger(入力中の半荘データが disabled になる)
    input = 'input'
    mode = 'mode'
    help = 'help'
    setting = 'setting'
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
    my_results = 'my_results'


def root(event: Event):
    print(f'receive {event.type} event')
    request_info_service.set_req_info(event)
    isEnabledReply = True

    try:
        if event.type == 'message':
            if event.message.type == 'text':
                textMessage(event)
            elif event.message.type == 'image':
                imageMessage(event)
        elif event.type == 'follow':
            follow_use_case.execute()
        elif event.type == 'unfollow':
            unfollow_use_case.execute()
            isEnabledReply = False
        elif event.type == 'join':
            join_group_use_case.execute()
        elif event.type == 'postback':
            postback(event)

    except BaseException as err:
        print(err)
        reply_service.add_message(str(err))

    if isEnabledReply:
        reply_service.reply(event)
    request_info_service.delete_req_info()


def textMessage(event: Event):
    """receive text message event"""
    if event.source.type == 'room' or event.source.type == 'group':
        routing_for_group_by_text(event)
    elif event.source.type == 'user':
        routing_by_text(event)
    else:
        print(
            f'error: message.source.type: {event.source.type}'
        )
        raise BaseException('this source type is not supported')


def imageMessage(event: Event):
    """receive image message event"""
    if event.source.type == 'room' or event.source.type == 'group':
        message_content = line_bot_api.get_message_content(
            event.message.id
        )
        input_result_from_image_use_case.execute(message_content.content)


def postback(event: Event):
    """postback event"""

    text: str = event.postback.data
    method = text[1:].split()[0]
    body = text[len(method) + 2:]
    if event.source.type == 'room' or event.source.type == 'group':
        routing_for_group_by_method(method, body)
    elif event.source.type == 'user':
        routing_by_method(method, body)


def routing_by_text(event: Event):
    """routing by text for personal chat"""
    text = event.message.text
    if (text[0] == '_') & (len(text) > 1):
        method = text[1:].split()[0]
        if method in [c.name for c in UCommands]:
            body = text[len(method) + 2:]
            routing_by_method(method, body)
            return
        else:
            reply_service.add_message(
                '使い方がわからない場合はメニューの中の「使い方」を押してください。'
            )
            return

    """routing by text on each mode"""
    """wait mode"""
    # if zoom url, register to group
    if '.zoom.us' in text:
        set_zoom_url_to_user_use_case.execute(text)
        return

    reply_service.add_message(
        message_service.get_wait_massage()
    )


def routing_by_method(method: str, body: str):
    """routing by method for personal chat"""

    # mode
    if method == UCommands.mode.name:
        reply_user_mode_use_case.execute()
    # exit
    elif method == UCommands.exit.name:
        user_exit_command_use_case.execute(
            request_info_service.req_line_user_id,
        )
    # payment
    elif method == UCommands.payment.name:
        reply_service.add_message('支払い機能は開発中です。')
    # analysis
    elif method == UCommands.analysis.name:
        reply_service.add_message('分析機能は開発中です。')
    # fortune
    elif method == UCommands.fortune.name:
        reply_fortune_use_case.execute()
    # history
    elif method == UCommands.history.name:
        reply_service.add_message('対戦履歴機能は開発中です。')
    # setting
    elif method == UCommands.setting.name:
        reply_service.add_message('個人設定機能は開発中です。')
    # help
    elif method == UCommands.help.name:
        reply_user_help_use_case.execute(UCommands)
    # github
    elif method == UCommands.github.name:
        reply_github_url_use_case.execute()
    # github
    elif method == UCommands.my_zoom.name:
        user_my_zoom_command_use_case.execute()


def routing_for_group_by_text(event: Event):
    """routing by text"""
    text = event.message.text
    if (text[0] == '_') & (len(text) > 1):
        method = text[1:].split()[0]
        if method in [c.name for c in RCommands]:
            body = text[len(method) + 2:]
            routing_for_group_by_method(method, body)
            return
        else:
            reply_service.add_message(
                '使い方がわからない場合は「_help」と入力してください。'
            )
            return

    """routing by text on each mode"""
    group_id = request_info_service.req_line_group_id
    current_mode = group_service.get_mode(group_id)
    """input mode"""
    if current_mode.value == GroupMode.input.value:
        add_point_by_text_use_case.execute(text)
        return

    """wait mode"""
    """if text is result, add result"""

    resultRows = [r for r in text.split('\n') if ':' in r]
    if len(resultRows) == 4:
        add_hanchan_by_points_text_use_case.execute(text)

    """if zoom url, register to group"""
    if '.zoom.us' in text:
        set_zoom_url_to_group_use_case.execute(text)


def routing_for_group_by_method(method, body):
    """routing by method"""
    # input
    if method == RCommands.input.name:
        start_input_use_case.execute()
    # start menu
    elif method == RCommands.start.name:
        reply_start_menu_use_case.execute()
    # mode
    elif method == RCommands.mode.name:
        reply_group_mode_use_case.execute()
    # exit
    elif method == RCommands.exit.name:
        group_quit_use_case.execute()
    # help
    elif method == RCommands.help.name:
        reply_group_help_use_case.execute(RCommands)
    # setting
    elif method == RCommands.setting.name:
        reply_group_settings_menu_use_case.execute(body)
    # results
    elif method == RCommands.results.name:
        reply_sum_hanchans_use_case.execute()
    # results by match id
    elif method == RCommands.match.name:
        reply_sum_hanchans__by_match_id_use_case.execute(body)
    # drop
    elif method == RCommands.drop.name:
        drop_hanchan_by_index_use_case.execute(int(body))
    # drop match
    elif method == RCommands.drop_m.name:
        disable_match_use_case.execute()
    # finish
    elif method == RCommands.finish.name:
        match_finish_use_case.execute()
    # fortune
    elif method == RCommands.fortune.name:
        reply_fortune_use_case.execute()
    # others menu
    elif method == RCommands.others.name:
        reply_others_menu_use_case.execute()
    # matches
    elif method == RCommands.matches.name:
        reply_matches_use_case.execute()
    # tobi
    elif method == RCommands.tobi.name:
        calculate_with_tobi_use_case.execute(
            tobashita_player_id=body
        )
    # my results
    elif method == RCommands.my_results.name:
        reply_my_results_use_case.execute()
    # add results
    elif method == RCommands.add_result.name:
        add_point_by_Json_text_use_case.execute(body)
    # update config
    elif method == RCommands.update_config.name:
        key = body.split(' ')[0]
        value = body.split(' ')[1]
        update_config_use_case.execute(
            key, value
        )
    # zoom
    elif method == RCommands.zoom.name:
        reply_group_zoom_url_use_case.execute()
    # my_zoom
    elif method == RCommands.my_zoom.name:
        set_my_zoom_url_to_group_use_case.execute()
    # sum_matches
    elif method == RCommands.sum_matches.name:
        args = body.split(' ')
        # while 'to' in args:
        #     index = args.index('to')
        #     if index != 0 and len(args) - 1 > index:
        #         args += [
        #             str(i) for i in range(
        #                 int(args[index - 1]),
        #                 int(args[index + 1]) + 1
        #             )
        #         ]
        #     args.remove('to')
        reply_sum_matches_by_ids_use_case.execute(args)
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
