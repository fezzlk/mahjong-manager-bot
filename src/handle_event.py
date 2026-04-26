"""LINE messaging API handler"""

import logging
from functools import wraps

from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import (
    FollowEvent,
    ImageMessageContent,
    JoinEvent,
    LeaveEvent,
    MessageEvent,
    PostbackEvent,
    TextMessageContent,
    UnfollowEvent,
)

import env_var
from application_service import (
    reply_service,
    request_info_service,
)

# ハンドラーを作成
handler = WebhookHandler(env_var.YOUR_CHANNEL_SECRET)
from routing_by_text_in_group_line import routing_by_text_in_group_line
from routing_by_text_in_personal_line import routing_by_text_in_personal_line
from use_cases.group_line.group_quit_use_case import GroupQuitUseCase
from use_cases.group_line.join_group_use_case import JoinGroupUseCase
from use_cases.personal_line.follow_use_case import FollowUseCase
from use_cases.personal_line.unfollow_use_case import UnfollowUseCase

logger = logging.getLogger(__name__)


def handle_event_decorator(function):
    @wraps(function)
    def handle_event(*args, **kwargs):
        event = args[0]
        logger.info("receipt an event: %s", event)

        try:
            request_info_service.set_req_info(event)
            function(args[0])

        except Exception as err:
            logger.exception("Unhandled exception in event handler")
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message=f"システムエラー: {type(err).__name__}: {err}",
            )
            reply_service.reset()
            reply_service.add_message(text="システムエラーが発生しました。")
        reply_service.reply(event)
        reply_service.reset()
        request_info_service.delete_req_info()

    return handle_event


@handler.add(FollowEvent)
@handle_event_decorator
def handle_follow(event):
    FollowUseCase().execute()


@handler.add(UnfollowEvent)
@handle_event_decorator
def handle_unfollow(event):
    UnfollowUseCase().execute()


@handler.add(JoinEvent)
@handle_event_decorator
def handle_join(event):
    JoinGroupUseCase().execute()


@handler.add(LeaveEvent)
@handle_event_decorator
def handle_leave(event):
    GroupQuitUseCase().execute()


@handler.add(MessageEvent, message=TextMessageContent)
@handle_event_decorator
def handle_text_message(event):
    if event.source.type in {"room", "group"}:
        routing_by_text_in_group_line()
    elif event.source.type == "user":
        routing_by_text_in_personal_line()
    else:
        raise ValueError("this source type is not supported")


@handler.add(MessageEvent, message=ImageMessageContent)
@handle_event_decorator
def handle_image_message(event):
    return


@handler.add(PostbackEvent)
@handle_event_decorator
def handle_postback(event):
    if event.source.type in {"room", "group"}:
        routing_by_text_in_group_line()
    elif event.source.type == "user":
        routing_by_text_in_personal_line()
