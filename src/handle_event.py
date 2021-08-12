"""
LINE messaging API handler
"""
from server import handler, router
from linebot.models import (
    FollowEvent,
    UnfollowEvent,
    JoinEvent,
    MessageEvent,
    TextMessage,
    ImageMessage,
    PostbackEvent,
)

@handler.add(FollowEvent)
def handle_follow(event):
    router.root(event)


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    router.root(event)


@handler.add(JoinEvent)
def handle_join(event):
    router.root(event)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    router.root(event)


@ handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    router.root(event)


@ handler.add(PostbackEvent)
def handle_postback(event):
    router.root(event)
