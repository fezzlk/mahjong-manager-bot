from enum import Enum

from application_service import (
    reply_service,
    request_info_service,
)

from domain_model.entities.group import GroupMode
from domain_service import (
    group_service,
)
from use_cases.common_line.reply_fortune_use_case import ReplyFortuneUseCase
from use_cases.common_line.reply_rank_histogram_use_case import ReplyRankHistogramUseCase
from use_cases.common_line.reply_rank_history_use_case import ReplyRankHistoryUseCase
from use_cases.group_line.add_point_by_text_use_case import AddPointByTextUseCase
from use_cases.group_line.add_chip_by_text_use_case import AddChipByTextUseCase
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
    # drop_m is defined but not yet implemented (DisableMatchUseCase pending)
    drop_m = "drop_m"
    add_result = "add_result"
    update_config = "update_config"
    # sum_matches is defined but not yet implemented (ReplySumMatchesByIdsUseCase pending)
    sum_matches = "sum_matches"
    my_results = "my_results"
    history = "history"
    chip_ok = "chip_ok"
    badai = "badai"
    # entry is defined but not yet implemented (LinkUserToGroupUseCase pending)
    entry = "entry"
    rank = "rank"
    rank_detail = "rank_detail"
    ranking = "ranking"


# Use a set for O(1) command lookup
_VALID_COMMANDS = {c.name for c in RCommands}


def routing_by_text_in_group_line():
    group_service.find_or_create(request_info_service.req_line_group_id)

    """routing by text"""
    command = request_info_service.command
    if command is not None:
        if command in _VALID_COMMANDS:
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


def routing_for_group_by_command(command):
    """Routing by command using dispatch table"""
    body = request_info_service.body

    def _update_config():
        key = body.split(" ")[0]
        value = body.split(" ")[1]
        UpdateGroupSettingsUseCase().execute(key, value)

    def _tobi():
        SubmitHanchanUseCase().execute(tobashita_player_id=body)

    _DISPATCH = {
        RCommands.input.name: lambda: StartInputUseCase().execute(),
        RCommands.start.name: lambda: ReplyStartMenuUseCase().execute(),
        RCommands.mode.name: lambda: ReplyGroupModeUseCase().execute(),
        RCommands.exit.name: lambda: ExitUseCase().execute(),
        RCommands.help.name: lambda: ReplyGroupHelpUseCase().execute(RCommands),
        RCommands.setting.name: lambda: ReplyGroupSettingsMenuUseCase().execute(body),
        RCommands.match.name: lambda: ReplyMatchByIndexUseCase().execute(body),
        RCommands.drop.name: lambda: DropHanchanByIndexUseCase().execute(body),
        RCommands.finish.name: lambda: FinishMatchUseCase().execute(),
        RCommands.finish_confirm.name: lambda: ReplyFinishConfirmUseCase().execute(),
        RCommands.fortune.name: lambda: ReplyFortuneUseCase().execute(),
        RCommands.others.name: lambda: ReplyOthersMenuUseCase().execute(),
        RCommands.active_match.name: lambda: ReplyHanchansOfActiveMatchUseCase().execute(),
        RCommands.matches.name: lambda: ReplyMatchesUseCase().execute(),
        RCommands.tobi.name: _tobi,
        RCommands.update_config.name: _update_config,
        RCommands.history.name: lambda: ReplyMultiHistoryUseCase().execute(),
        RCommands.chip_ok.name: lambda: FinishInputChipUseCase().execute(),
        RCommands.badai.name: lambda: ReplyApplyBadaiUseCase().execute(body),
        RCommands.rank.name: lambda: ReplyRankHistoryUseCase().execute(),
        RCommands.rank_detail.name: lambda: ReplyRankHistogramUseCase().execute(),
        RCommands.ranking.name: lambda: ReplyRankingTableUseCase().execute(),
        # drop_m (DisableMatchUseCase), entry (LinkUserToGroupUseCase),
        # sum_matches (ReplySumMatchesByIdsUseCase), add_result, my_results:
        # intentionally not yet implemented — stub commands reserved for future use
    }

    handler = _DISPATCH.get(command)
    if handler:
        handler()
