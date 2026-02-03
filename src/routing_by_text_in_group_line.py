from enum import Enum

from application_service import (
    reply_service,
    request_info_service,
)

# from use_cases.group_line.link_user_to_group_use_case import LinkUserToGroupUseCase
from domain_model.entities.group import GroupMode
from domain_service import (
    group_service,
)
from use_cases.common_line.reply_fortune_use_case import ReplyFortuneUseCase
from use_cases.common_line.reply_rank_histogram_use_case import ReplyRankHistogramUseCase
from use_cases.common_line.reply_rank_history_use_case import ReplyRankHistoryUseCase

# from use_cases.group_line.add_hanchan_by_points_text_use_case import AddHanchanByPointsTextUseCase
from use_cases.group_line.add_point_by_text_use_case import AddPointByTextUseCase
from use_cases.group_line.add_chip_by_text_use_case import AddChipByTextUseCase

# from use_cases.group_line.reply_sum_matches_by_ids_use_case import ReplySumMatchesByIdsUseCase
# from use_cases.group_line.DisableMatchUseCase import DisableMatchUseCase
from use_cases.group_line.drop_hanchan_by_index_use_case import DropHanchanByIndexUseCase
from use_cases.group_line.exit_use_case import ExitUseCase
from use_cases.group_line.finish_input_chip_use_case import FinishInputChipUseCase
from use_cases.group_line.finish_match_use_case import FinishMatchUseCase
from use_cases.group_line.reply_apply_badai_use_case import ReplyApplyBadaiUseCase
from use_cases.group_line.reply_finish_confirm_use_case import ReplyFinishConfirmUseCase
from use_cases.group_line.reply_group_help_use_case import ReplyGroupHelpUseCase
from use_cases.group_line.reply_group_mode_use_case import ReplyGroupModeUseCase
from use_cases.group_line.reply_group_settings_menu_use_case import (
    ReplyGroupSettingsMenuUseCase,
)
from use_cases.group_line.reply_hanchans_of_active_match_use_case import (
    ReplyHanchansOfActiveMatchUseCase,
)
from use_cases.group_line.reply_match_by_index_use_case import ReplyMatchByIndexUseCase
from use_cases.group_line.reply_matches_use_case import ReplyMatchesUseCase
from use_cases.group_line.reply_multi_history_use_case import ReplyMultiHistoryUseCase
from use_cases.group_line.reply_others_menu_use_case import ReplyOthersMenuUseCase
from use_cases.group_line.reply_ranking_table_use_case import ReplyRankingTableUseCase
from use_cases.group_line.reply_start_menu_use_case import ReplyStartMenuUseCase
from use_cases.group_line.start_input_use_case import StartInputUseCase
from use_cases.group_line.submit_hanchan_use_case import SubmitHanchanUseCase
from use_cases.group_line.update_group_settings_use_case import UpdateGroupSettingsUseCase


class RCommands(Enum):
    """Commands for group"""

    start = "start"
    exit = "exit"  # danger(入力中の半荘データが disabled になる)
    input = "input"
    mode = "mode"
    help = "help"
    setting = "setting"
    active_match = "active_match"
    finish = "finish"
    finish_confirm = "finish_confirm"
    fortune = "fortune"
    others = "others"
    matches = "matches"
    match = "match"
    tobi = "tobi"
    drop = "drop"
    drop_m = "drop_m"
    add_result = "add_result"
    update_config = "update_config"
    sum_matches = "sum_matches"
    my_results = "my_results"
    history = "history"
    chip_ok = "chip_ok"
    badai = "badai"
    entry = "entry"
    rank = "rank"
    rank_detail = "rank_detail"
    ranking = "ranking"


def routing_by_text_in_group_line():
    group_service.find_or_create(request_info_service.req_line_group_id)

    """routing by text"""
    command = request_info_service.command
    if command is not None:
        if command in [c.name for c in RCommands]:
            routing_for_group_by_command(command)
            return
        reply_service.add_message(
            "使い方がわからない場合は「_help」と入力してください。",
        )
        return

    """routing by text on each mode"""
    group_id = request_info_service.req_line_group_id
    current_mode = group_service.get_mode(group_id)
    """input mode"""
    if current_mode == GroupMode.input.value:
        AddPointByTextUseCase().execute(request_info_service.message)
        return
    """chip input mode"""
    if current_mode == GroupMode.chip_input.value:
        AddChipByTextUseCase().execute(request_info_service.message)
        return

    """wait mode"""
    """if text is result, add result"""

    # resultRows = [r for r in text.split('\n') if ':' in r]
    # if len(resultRows) == 4:
    #     AddHanchanByPointsTextUseCase().execute(text)


def routing_for_group_by_command(command):
    """Routing by command"""
    body = request_info_service.body
    # input
    if command == RCommands.input.name:
        StartInputUseCase().execute()
    # start menu
    elif command == RCommands.start.name:
        ReplyStartMenuUseCase().execute()
    # mode
    elif command == RCommands.mode.name:
        ReplyGroupModeUseCase().execute()
    # exit
    elif command == RCommands.exit.name:
        ExitUseCase().execute()
    # help
    elif command == RCommands.help.name:
        ReplyGroupHelpUseCase().execute(RCommands)
    # setting
    elif command == RCommands.setting.name:
        ReplyGroupSettingsMenuUseCase().execute(body)
    # match detail by index
    elif command == RCommands.match.name:
        ReplyMatchByIndexUseCase().execute(body)
    # drop
    elif command == RCommands.drop.name:
        DropHanchanByIndexUseCase().execute(body)
    # drop match
    # elif command == RCommands.drop_m.name:
    #     DisableMatchUseCase().execute()
    # finish
    elif command == RCommands.finish.name:
        FinishMatchUseCase().execute()
    # finish_confirm
    elif command == RCommands.finish_confirm.name:
        ReplyFinishConfirmUseCase().execute()
    # fortune
    elif command == RCommands.fortune.name:
        ReplyFortuneUseCase().execute()
    # others menu
    elif command == RCommands.others.name:
        ReplyOthersMenuUseCase().execute()
    # active_match
    elif command == RCommands.active_match.name:
        ReplyHanchansOfActiveMatchUseCase().execute()
    # matches
    elif command == RCommands.matches.name:
        ReplyMatchesUseCase().execute()
    # tobi
    elif command == RCommands.tobi.name:
        SubmitHanchanUseCase().execute(
            tobashita_player_id=body,
        )
    # update config
    elif command == RCommands.update_config.name:
        key = body.split(" ")[0]
        value = body.split(" ")[1]
        UpdateGroupSettingsUseCase().execute(
            key,
            value,
        )
    # history
    elif command == RCommands.history.name:
        ReplyMultiHistoryUseCase().execute()
    # chip_ok
    elif command == RCommands.chip_ok.name:
        FinishInputChipUseCase().execute()
    # badai
    elif command == RCommands.badai.name:
        ReplyApplyBadaiUseCase().execute(body)
    # rank
    elif command == RCommands.rank.name:
        ReplyRankHistoryUseCase().execute()
    # rank detail
    elif command == RCommands.rank_detail.name:
        ReplyRankHistogramUseCase().execute()
    elif command == RCommands.ranking.name:
        ReplyRankingTableUseCase().execute()

    # # entry
    # elif command == RCommands.entry.name:
    #     LinkUserToGroupUseCase().execute()
    # sum_matches
    # elif command == RCommands.sum_matches.name:
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
