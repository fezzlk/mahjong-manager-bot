"""
Application root
If '$ flask run' is executed, this file is call at first.
"""
import os

import set_local_env  # for local dev env

from db_setting import Engine
from models import Base

from flask import Flask, request, abort, g, render_template
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
def index():
    # テーブルの作成
    # Base.metadata.drop_all(bind=Engine)
    # Base.metadata.create_all(bind=Engine)
    data = {}
    data['name'] = "Hoge"
    return render_template('index.html', title='index', data=data)


@app.route('/users')
def users():
    data = services.user_service.get_all()
    keys = ['id', 'name', 'user_id', 'mode', 'rooms', 'matches']
    return render_template(
        'table.html',
        title='users',
        keys=keys,
        data=data
    )


@app.route('/rooms')
def rooms():
    data = services.room_service.get_all()
    keys = ['id', 'room_id', 'mode', 'users']
    return render_template(
        'table.html',
        title='rooms',
        keys=keys,
        data=data
    )


@app.route('/results')
def results():
    data = services.results_service.get_all()
    for d in data:
        print(d.result)
    keys = ['id', 'room_id', 'points', 'result', 'match_id', 'status']
    return render_template(
        'table.html',
        title='results',
        keys=keys,
        data=data
    )


@app.route('/matches')
def matches():
    data = services.matches_service.get_all()
    keys = ['id', 'room_id', 'result_ids', 'created_at', 'status', 'users']
    return render_template(
        'table.html',
        title='matches',
        keys=keys,
        data=data
    )


@app.route('/configs')
def configs():
    data = services.config_service.get_all_r()
    keys = ['id', 'key', 'value', 'target_id']
    return render_template(
        'table.html',
        title='configs',
        keys=keys,
        data=data
    )


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
