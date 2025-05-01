"""LINE messaging API handler
"""
import traceback

from linebot.models import (
    FollowEvent,
    ImageMessage,
    JoinEvent,
    LeaveEvent,
    MessageEvent,
    PostbackEvent,
    TextMessage,
    UnfollowEvent,
)

# from use_cases.group_line.InputResultFromImageUseCase import (
#     InputResultFromImageUseCase)
import env_var
from apis.root import handler
from ApplicationService import (
    reply_service,
    request_info_service,
)
from messaging_api_setting import line_bot_api
from routing_by_text_in_group_line import routing_by_text_in_group_line
from routing_by_text_in_personal_line import routing_by_text_in_personal_line
from use_cases.group_line.GroupQuitUseCase import GroupQuitUseCase
from use_cases.group_line.JoinGroupUseCase import JoinGroupUseCase
from use_cases.personal_line.FollowUseCase import FollowUseCase
from use_cases.personal_line.UnfollowUseCase import UnfollowUseCase


def handle_event_decorater(function):
    def handle_event(*args, **kwargs):
        event = args[0]
        print("receipt an event:")
        print(event)

        try:
            request_info_service.set_req_info(event)
            function(args[0])

        except BaseException as err:
            traceback.print_exc()
            profile = line_bot_api.get_profile(
                request_info_service.req_line_user_id,
            )
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message=f"From: {profile.display_name}\n{request_info_service.message}",
            )
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message=str(err),
            )
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message="heroku logs -a mahjong-manager -t",
            )
            reply_service.reset()
            reply_service.add_message(text="システムエラーが発生しました。")
        reply_service.reply(event)
        reply_service.reset()
        request_info_service.delete_req_info()

    return handle_event


@handler.add(FollowEvent)
@handle_event_decorater
def handle_follow(event):
    FollowUseCase().execute()


@handler.add(UnfollowEvent)
@handle_event_decorater
def handle_unfollow(event):
    UnfollowUseCase().execute()


@handler.add(JoinEvent)
@handle_event_decorater
def handle_join(event):
    JoinGroupUseCase().execute()


@handler.add(LeaveEvent)
@handle_event_decorater
def handle_leave(event):
    GroupQuitUseCase().execute()


@handler.add(MessageEvent, message=TextMessage)
@handle_event_decorater
def handle_text_message(event):
    if event.source.type == "room" or event.source.type == "group":
        routing_by_text_in_group_line()
    elif event.source.type == "user":
        routing_by_text_in_personal_line()
    else:
        raise BaseException("this source type is not supported")


@handler.add(MessageEvent, message=ImageMessage)
@handle_event_decorater
def handle_image_message(event):
    # if event.source.type == 'room' or event.source.type == 'group':
    #     InputResultFromImageUseCase().execute(event)
    # else:
    # raise BaseException('this source type is not supported')
    return


@handler.add(PostbackEvent)
@handle_event_decorater
def handle_postback(event):
    if event.source.type == "room" or event.source.type == "group":
        routing_by_text_in_group_line()
    elif event.source.type == "user":
        routing_by_text_in_personal_line()
