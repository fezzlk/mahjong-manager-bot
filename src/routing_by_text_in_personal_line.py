from enum import Enum

from application_service import (
    message_service,
    reply_service,
    request_info_service,
)
from domain_service import user_service
from use_cases.common_line.reply_fortune_use_case import ReplyFortuneUseCase
from use_cases.common_line.reply_fortune_yaku_use_case import ReplyFortuneYakuUseCase
from use_cases.common_line.reply_github_url_use_case import ReplyGitHubUrlUseCase
from use_cases.common_line.reply_rank_histogram_use_case import (
    ReplyRankHistogramUseCase,
)
from use_cases.common_line.reply_rank_history_use_case import ReplyRankHistoryUseCase
from use_cases.personal_line.reply_history_use_case import ReplyHistoryUseCase
from use_cases.personal_line.reply_token_use_case import ReplyTokenUseCase
from use_cases.personal_line.reply_url_use_case import ReplyUrlUseCase
from use_cases.personal_line.reply_user_help_use_case import ReplyUserHelpUseCase
from use_cases.personal_line.reply_user_mode_use_case import ReplyUserModeUseCase
from use_cases.personal_line.request_link_line_web_use_case import (
    RequestLinkLineWebUseCase,
)
from use_cases.personal_line.user_exit_command_use_case import UserExitCommandUseCase
from use_cases.group_line.migrate_group_use_case import MigrateGroupUseCase


class UCommands(Enum):
    """Commands for personal user"""

    exit = "exit"
    mode = "mode"
    payment = "payment"
    analysis = "analysis"
    fortune = "fortune"
    fortune_yaku = "fortune_yaku"
    history = "history"
    help = "help"
    setting = "setting"
    github = "github"
    token = "token"
    url = "url"
    rank = "rank"
    rank_detail = "rank_detail"
    personal_history = "personal_history"
    personal_migrate = "personal_migrate"


# Use a set for O(1) command lookup
_VALID_COMMANDS = {c.name for c in UCommands}


def routing_by_text_in_personal_line():
    if (
        user_service.find_one_by_line_user_id(request_info_service.req_line_user_id)
        is None
    ):
        reply_service.add_message(
            "ユーザーが登録されていません。友達追加してください。",
        )
        return

    """routing by text for personal chat"""
    command = request_info_service.command
    if command is not None:
        if command in _VALID_COMMANDS:
            routing_by_command(command)
            return
        reply_service.add_message(
            "使い方がわからない場合はメニューの中の「使い方」を押してください。",
        )
        return

    """routing by text on each mode"""
    """wait mode"""

    parts = request_info_service.message.split()
    if parts and parts[0] == "アカウント連携":
        RequestLinkLineWebUseCase().execute()
        return

    reply_service.add_message(
        message_service.get_wait_massage(),
    )


def routing_by_command(command: str):
    """Routing by command for personal chat using dispatch table"""
    req_line_user_id = request_info_service.req_line_user_id

    dispatch = {
        UCommands.mode.name: lambda: ReplyUserModeUseCase().execute(),
        UCommands.exit.name: lambda: UserExitCommandUseCase().execute(req_line_user_id),
        UCommands.payment.name: lambda: reply_service.add_message("支払い機能は開発中です。"),
        UCommands.analysis.name: lambda: reply_service.add_message("分析機能は開発中です。"),
        UCommands.fortune.name: lambda: ReplyFortuneUseCase().execute(),
        UCommands.fortune_yaku.name: lambda: ReplyFortuneYakuUseCase().execute(),
        UCommands.history.name: lambda: ReplyHistoryUseCase().execute(),
        UCommands.setting.name: lambda: reply_service.add_message("個人設定機能は開発中です。"),
        UCommands.help.name: lambda: ReplyUserHelpUseCase().execute(),
        UCommands.github.name: lambda: ReplyGitHubUrlUseCase().execute(),
        UCommands.token.name: lambda: ReplyTokenUseCase().execute(),
        UCommands.url.name: lambda: ReplyUrlUseCase().execute(),
        UCommands.rank.name: lambda: ReplyRankHistoryUseCase().execute(),
        UCommands.rank_detail.name: lambda: ReplyRankHistogramUseCase().execute(),
        UCommands.personal_history.name: lambda: ReplyHistoryUseCase().execute(),
        UCommands.personal_migrate.name: lambda: MigrateGroupUseCase().execute_personal(),
    }

    handler = dispatch.get(command)
    if handler:
        handler()
