"""
LINE messaging API handler
"""
from apis.root import handler
from routing_by_text_in_group_line import routing_by_text_in_group_line
from routing_by_text_in_personal_line import routing_by_text_in_personal_line
from linebot.models import (
    FollowEvent,
    UnfollowEvent,
    JoinEvent,
    MessageEvent,
    TextMessage,
    ImageMessage,
    PostbackEvent,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from use_cases.personal_line.FollowUseCase import FollowUseCase
from use_cases.personal_line.UnfollowUseCase import UnfollowUseCase
from use_cases.group_line.JoinGroupUseCase import JoinGroupUseCase
# from use_cases.group_line.InputResultFromImageUseCase import (
#     InputResultFromImageUseCase)
import env_var
import traceback


def handle_event_decorater(function):
    def handle_event(*args, **kwargs):
        event = args[0]
        print('receipt an event:')
        print(event)

        try:
            request_info_service.set_req_info(event)
            function(args[0])

        except BaseException as err:
            traceback.print_exc()
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message=str(err),
            )
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message='heroku logs -a mahjong-manager -t',
            )
            reply_service.reset()
            reply_service.add_message(text='システムエラーが発生しました。')
        reply_service.reply(event)
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


@handler.add(MessageEvent, message=TextMessage)
@handle_event_decorater
def handle_text_message(event):
    text = event.message.text
    if event.source.type == 'room' or event.source.type == 'group':
        routing_by_text_in_group_line(text)
    elif event.source.type == 'user':
        routing_by_text_in_personal_line(text)
    else:
        raise BaseException('this source type is not supported')


@ handler.add(MessageEvent, message=ImageMessage)
@ handle_event_decorater
def handle_image_message(event):
    # if event.source.type == 'room' or event.source.type == 'group':
    #     InputResultFromImageUseCase().execute(event)
    # else:
    # raise BaseException('this source type is not supported')
    return


@ handler.add(PostbackEvent)
@ handle_event_decorater
def handle_postback(event):
    text = event.postback.data
    if event.source.type == 'room' or event.source.type == 'group':
        routing_by_text_in_group_line(text)
    elif event.source.type == 'user':
        routing_by_text_in_personal_line(text)
