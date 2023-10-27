from enum import Enum

from DomainService import (
    group_service,
)

from ApplicationService import (
    request_info_service,
    reply_service,
)
from use_cases.common_line.ReplyFortuneUseCase import ReplyFortuneUseCase
from use_cases.group_line.SubmitHanchanUseCase import SubmitHanchanUseCase

from use_cases.group_line.ExitUseCase import ExitUseCase
from use_cases.group_line.ReplyGroupHelpUseCase import ReplyGroupHelpUseCase
from use_cases.group_line.ReplyGroupSettingsMenuUseCase import ReplyGroupSettingsMenuUseCase
from use_cases.group_line.ReplyStartMenuUseCase import ReplyStartMenuUseCase
from use_cases.group_line.ReplyOthersMenuUseCase import ReplyOthersMenuUseCase
from use_cases.group_line.ReplyGroupModeUseCase import ReplyGroupModeUseCase
from use_cases.group_line.ReplyApplyBadaiUseCase import ReplyApplyBadaiUseCase

# from use_cases.group_line.AddHanchanByPointsTextUseCase import AddHanchanByPointsTextUseCase
from use_cases.group_line.AddPointByTextUseCase import AddPointByTextUseCase
from use_cases.group_line.AddTipByTextUseCase import AddTipByTextUseCase
from use_cases.group_line.StartInputUseCase import StartInputUseCase

from use_cases.group_line.ReplyMatchesUseCase import ReplyMatchesUseCase
from use_cases.group_line.ReplyMatchByIndexUseCase import ReplyMatchByIndexUseCase
# from use_cases.group_line.ReplySumMatchesByIdsUseCase import ReplySumMatchesByIdsUseCase
# from use_cases.group_line.DisableMatchUseCase import DisableMatchUseCase
from use_cases.group_line.DropHanchanByIndexUseCase import DropHanchanByIndexUseCase
from use_cases.group_line.FinishMatchUseCase import FinishMatchUseCase
from use_cases.group_line.ReplyFinishConfirmUseCase import ReplyFinishConfirmUseCase
from use_cases.group_line.FinishInputTipUseCase import FinishInputTipUseCase

from use_cases.group_line.UpdateGroupSettingsUseCase import UpdateGroupSettingsUseCase
from use_cases.group_line.ReplyMultiHistoryUseCase import ReplyMultiHistoryUseCase
# from use_cases.group_line.LinkUserToGroupUseCase import LinkUserToGroupUseCase

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
    finish_confirm = 'finish_confirm'
    fortune = 'fortune'
    others = 'others'
    matches = 'matches'
    match = 'match'
    tobi = 'tobi'
    drop = 'drop'
    drop_m = 'drop_m'
    add_result = 'add_result'
    update_config = 'update_config'
    sum_matches = 'sum_matches'
    my_results = 'my_results'
    history = 'history'
    tip_ok = 'tip_ok'
    badai = 'badai'
    entry = 'entry'


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
    if current_mode == GroupMode.input.value:
        AddPointByTextUseCase().execute(text)
        return
    """tip input mode"""
    if current_mode == GroupMode.tip_input.value:
        AddTipByTextUseCase().execute(text)
        return

    """wait mode"""
    """if text is result, add result"""

    # resultRows = [r for r in text.split('\n') if ':' in r]
    # if len(resultRows) == 4:
    #     AddHanchanByPointsTextUseCase().execute(text)


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
        ExitUseCase().execute()
    # help
    elif method == RCommands.help.name:
        ReplyGroupHelpUseCase().execute(RCommands)
    # setting
    elif method == RCommands.setting.name:
        ReplyGroupSettingsMenuUseCase().execute(body)
    # match detail by index
    elif method == RCommands.match.name:
        ReplyMatchByIndexUseCase().execute(body)
    # drop
    elif method == RCommands.drop.name:
        DropHanchanByIndexUseCase().execute(int(body))
    # drop match
    # elif method == RCommands.drop_m.name:
    #     DisableMatchUseCase().execute()
    # finish
    elif method == RCommands.finish.name:
        FinishMatchUseCase().execute()
    # finish_confirm
    elif method == RCommands.finish_confirm.name:
        ReplyFinishConfirmUseCase().execute()
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
        SubmitHanchanUseCase().execute(
            tobashita_player_id=body
        )
    # update config
    elif method == RCommands.update_config.name:
        key = body.split(' ')[0]
        value = body.split(' ')[1]
        UpdateGroupSettingsUseCase().execute(
            key, value
        )
    # history
    elif method == RCommands.history.name:
        ReplyMultiHistoryUseCase().execute()
    # tip_ok
    elif method == RCommands.tip_ok.name:
        FinishInputTipUseCase().execute()
    # badai
    elif method == RCommands.badai.name:
        ReplyApplyBadaiUseCase().execute(body)
    # # entry
    # elif method == RCommands.entry.name:
    #     LinkUserToGroupUseCase().execute()
    # sum_matches
    # elif method == RCommands.sum_matches.name:
    #     args = body.split(' ')
    #     # while 'to' in args:
    #     #     index = args.index('to')
    #     #     if index != 0 and len(args) - 1 > index:
    #     #         args += [
    #     #             str(i) for i in range(
    #     #                 int(args[index - 1]),
    #     #                 int(args[index + 1]) + 1
    #     #             )
    #     #         ]
    #     #     args.remove('to')
    #     ReplySumMatchesByIdsUseCase().execute(args)

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
