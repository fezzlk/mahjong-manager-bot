"""
Application root
If '$ flask run' is executed, this file is call at first.
"""
import os

import set_local_env  # for local dev env

from db_setting import Engine
from models import Base

from flask import Flask, request, abort, g
from linebot import LineBotApi, WebhookHandler, exceptions
from linebot.models import (
    FollowEvent,
    UnfollowEvent,
    JoinEvent,
    MessageEvent,
    TextMessage,
    ImageMessage,
    PostbackEvent,
)

from router import Router
from services import Services

"""define LINE bot handler"""
handler = WebhookHandler(os.environ["YOUR_CHANNEL_SECRET"])

app = Flask(__name__)

services = Services(app)
router = Router(services)


@app.route('/')
def hello_world():
    # テーブルの作成
    Base.metadata.drop_all(bind=Engine)
    Base.metadata.create_all(bind=Engine)
    return "hello world."


@app.route('/create')
def create_table():
    # テーブルの作成
    Base.metadata.create_all(bind=Engine)
    return "create table"


"""
receive action from LINE
"""


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except exceptions.InvalidSignatureError:
        abort(400)
    return 'OK'


"""
handle events
"""


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


if __name__ == "__main__":
    app.run()
