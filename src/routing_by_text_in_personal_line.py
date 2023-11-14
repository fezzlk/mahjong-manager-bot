from enum import Enum

from ApplicationService import (
    request_info_service,
    reply_service,
    message_service,
)
from use_cases.personal_line.ReplyTokenUseCase import ReplyTokenUseCase
from use_cases.personal_line.ReplyUrlUseCase import ReplyUrlUseCase
from use_cases.personal_line.UserExitCommandUseCase import UserExitCommandUseCase
from use_cases.personal_line.ReplyUserHelpUseCase import ReplyUserHelpUseCase
from use_cases.personal_line.ReplyUserModeUseCase import ReplyUserModeUseCase
from use_cases.common_line.ReplyFortuneUseCase import ReplyFortuneUseCase
from use_cases.common_line.ReplyGitHubUrlUseCase import ReplyGitHubUrlUseCase
from use_cases.common_line.ReplyRankHistoryUseCase import ReplyRankHistoryUseCase
from use_cases.personal_line.ReplyHistoryUseCase import ReplyHistoryUseCase
from use_cases.personal_line.RequestLinkLineWebUseCase import RequestLinkLineWebUseCase


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
    token = 'token'
    url = 'url'
    rank = 'rank'


def routing_by_text_in_personal_line(text: str):
    """routing by text for personal chat"""
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

    if 'アカウント連携' == text.split()[0]:
        RequestLinkLineWebUseCase().execute()
        return

    reply_service.add_message(
        message_service.get_wait_massage()
    )


def routing_by_method(method: str, body: str):
    """routing by method for personal chat"""

    # mode
    if method == UCommands.mode.name:
        ReplyUserModeUseCase().execute()
    # exit
    elif method == UCommands.exit.name:
        UserExitCommandUseCase().execute(
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
        ReplyFortuneUseCase().execute()
    # history
    elif method == UCommands.history.name:
        ReplyHistoryUseCase().execute()
    # setting
    elif method == UCommands.setting.name:
        reply_service.add_message('個人設定機能は開発中です。')
    # help
    elif method == UCommands.help.name:
        ReplyUserHelpUseCase().execute(UCommands)
    # github
    elif method == UCommands.github.name:
        ReplyGitHubUrlUseCase().execute()
    # token
    elif method == UCommands.token.name:
        ReplyTokenUseCase().execute()
    # url
    elif method == UCommands.url.name:
        ReplyUrlUseCase().execute()
    # rank
    elif method == UCommands.rank.name:
        ReplyRankHistoryUseCase().execute()
