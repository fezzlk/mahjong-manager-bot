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
from use_cases.common_line.reply_rank_histogram_use_case import ReplyRankHistogramUseCase
from use_cases.common_line.reply_rank_history_use_case import ReplyRankHistoryUseCase
from use_cases.personal_line.reply_history_use_case import ReplyHistoryUseCase
from use_cases.personal_line.reply_token_use_case import ReplyTokenUseCase
from use_cases.personal_line.reply_url_use_case import ReplyUrlUseCase
from use_cases.personal_line.reply_user_help_use_case import ReplyUserHelpUseCase
from use_cases.personal_line.reply_user_mode_use_case import ReplyUserModeUseCase
from use_cases.personal_line.request_link_line_web_use_case import RequestLinkLineWebUseCase
from use_cases.personal_line.user_exit_command_use_case import UserExitCommandUseCase


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
        if command in [c.name for c in UCommands]:
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
    """Routing by command for personal chat"""
    # mode
    if command == UCommands.mode.name:
        ReplyUserModeUseCase().execute()
    # exit
    elif command == UCommands.exit.name:
        UserExitCommandUseCase().execute(
            request_info_service.req_line_user_id,
        )
    # payment
    elif command == UCommands.payment.name:
        reply_service.add_message("支払い機能は開発中です。")
    # analysis
    elif command == UCommands.analysis.name:
        reply_service.add_message("分析機能は開発中です。")
    # fortune
    elif command == UCommands.fortune.name:
        ReplyFortuneUseCase().execute()
    # fortune_yaku
    elif command == UCommands.fortune_yaku.name:
        ReplyFortuneYakuUseCase().execute()
    # history
    elif command == UCommands.history.name:
        ReplyHistoryUseCase().execute()
    # setting
    elif command == UCommands.setting.name:
        reply_service.add_message("個人設定機能は開発中です。")
    # help
    elif command == UCommands.help.name:
        ReplyUserHelpUseCase().execute()
    # github
    elif command == UCommands.github.name:
        ReplyGitHubUrlUseCase().execute()
    # token
    elif command == UCommands.token.name:
        ReplyTokenUseCase().execute()
    # url
    elif command == UCommands.url.name:
        ReplyUrlUseCase().execute()
    # rank
    elif command == UCommands.rank.name:
        ReplyRankHistoryUseCase().execute()
    # rank detail
    elif command == UCommands.rank_detail.name:
        ReplyRankHistogramUseCase().execute()
