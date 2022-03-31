from enum import Enum

from DomainService import (
    group_service,
)

from ApplicationService import (
    request_info_service,
    reply_service,
)
from use_cases.common_line.ReplyFortuneUseCase import ReplyFortuneUseCase
from use_cases.group_line.CalculateUseCase import CalculateUseCase

from use_cases.group_line.GroupQuitUseCase import GroupQuitUseCase
from use_cases.group_line.SetZoomUrlToGroupUseCase import SetZoomUrlToGroupUseCase
from use_cases.group_line.SetMyZoomUrlToGroupUseCase import SetMyZoomUrlToGroupUseCase
from use_cases.group_line.ReplyGroupHelpUseCase import ReplyGroupHelpUseCase
from use_cases.group_line.ReplyGroupSettingsMenuUseCase import ReplyGroupSettingsMenuUseCase
from use_cases.group_line.ReplyStartMenuUseCase import ReplyStartMenuUseCase
from use_cases.group_line.ReplyOthersMenuUseCase import ReplyOthersMenuUseCase
from use_cases.group_line.ReplyGroupModeUseCase import ReplyGroupModeUseCase
from use_cases.group_line.ReplyGroupZoomUrlUseCase import ReplyGroupZoomUrlUseCase

from use_cases.group_line.AddHanchanByPointsTextUseCase import AddHanchanByPointsTextUseCase
from use_cases.group_line.AddPointByTextUseCase import AddPointByTextUseCase
from use_cases.group_line.StartInputUseCase import StartInputUseCase
from use_cases.group_line.ReplySumHanchansUseCase import ReplySumHanchansUseCase

from use_cases.group_line.ReplyMatchesUseCase import ReplyMatchesUseCase
from use_cases.group_line.ReplySumHanchansByMatchIdUseCase import ReplySumHanchansByMatchIdUseCase
from use_cases.group_line.ReplySumMatchesByIdsUseCase import ReplySumMatchesByIdsUseCase
from use_cases.group_line.DisableMatchUseCase import DisableMatchUseCase
from use_cases.group_line.DropHanchanByIndexUseCase import DropHanchanByIndexUseCase
from use_cases.group_line.MatchFinishUseCase import MatchFinishUseCase

from use_cases.group_line.ReplyMyResultsUseCase import ReplyMyResultsUseCase

from use_cases.group_line.UpdateGroupConfigUseCase import UpdateGroupConfigUseCase

from DomainModel.entities.Group import GroupMode


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


def routing_by_text_in_group_line(text: str):
    """routing by text"""
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
        AddPointByTextUseCase().execute(text)
        return

    """wait mode"""
    """if text is result, add result"""

    resultRows = [r for r in text.split('\n') if ':' in r]
    if len(resultRows) == 4:
        AddHanchanByPointsTextUseCase().execute(text)

    """if zoom url, register to group"""
    if '.zoom.us' in text:
        SetZoomUrlToGroupUseCase().execute(text)


def routing_for_group_by_method(method, body):
    """routing by method"""
    # input
    if method == RCommands.input.name:
        StartInputUseCase().execute()
    # start menu
    elif method == RCommands.start.name:
        ReplyStartMenuUseCase().execute()
    # mode
    elif method == RCommands.mode.name:
        ReplyGroupModeUseCase().execute()
    # exit
    elif method == RCommands.exit.name:
        GroupQuitUseCase().execute()
    # help
    elif method == RCommands.help.name:
        ReplyGroupHelpUseCase().execute(RCommands)
    # setting
    elif method == RCommands.setting.name:
        ReplyGroupSettingsMenuUseCase().execute(body)
    # results
    elif method == RCommands.results.name:
        ReplySumHanchansUseCase().execute()
    # results by match id
    elif method == RCommands.match.name:
        ReplySumHanchansByMatchIdUseCase().execute(body)
    # drop
    elif method == RCommands.drop.name:
        DropHanchanByIndexUseCase().execute(int(body))
    # drop match
    elif method == RCommands.drop_m.name:
        DisableMatchUseCase().execute()
    # finish
    elif method == RCommands.finish.name:
        MatchFinishUseCase().execute()
    # fortune
    elif method == RCommands.fortune.name:
        ReplyFortuneUseCase().execute()
    # others menu
    elif method == RCommands.others.name:
        ReplyOthersMenuUseCase().execute()
    # matches
    elif method == RCommands.matches.name:
        ReplyMatchesUseCase().execute()
    # tobi
    elif method == RCommands.tobi.name:
        CalculateUseCase().execute(
            tobashita_player_id=body
        )
    # my results
    elif method == RCommands.my_results.name:
        ReplyMyResultsUseCase().execute()
    # update config
    elif method == RCommands.update_config.name:
        key = body.split(' ')[0]
        value = body.split(' ')[1]
        UpdateGroupConfigUseCase().execute(
            key, value
        )
    # zoom
    elif method == RCommands.zoom.name:
        ReplyGroupZoomUrlUseCase().execute()
    # my_zoom
    elif method == RCommands.my_zoom.name:
        SetMyZoomUrlToGroupUseCase().execute()
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
        ReplySumMatchesByIdsUseCase().execute(args)
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
