"""
Application root
If '$ flask run' is executed, this file is call at first.
"""
import os

import set_local_env  # for local dev env

from db_setting import Engine
from models import Base

from flask import Flask, request, abort, logging, g
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
from flask_sqlalchemy import SQLAlchemy

from router import Router
from services import Services

"""define LINE bot handler"""
handler = WebhookHandler(os.environ["YOUR_CHANNEL_SECRET"])

app = Flask(__name__)
logger = logging.create_logger(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)

services = Services(logger)
services.app_service.set_db(db)
router = Router(services)


@app.route('/')
def hello_world():
    # テーブルの作成
    Base.metadata.create_all(bind=Engine)
    logger.info('lllllllllllll')
    # Base.metadata.drop_all(bind=Engine)
    # Base.metadata.create_all(bind=Engine)
    return "hello world."


@app.route('/create')
def create_table():
    # テーブルの作成
    Base.metadata.create_all(bind=Engine)
    return "create table"


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
    logger.info('follow')
    router.follow(event)


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    logger.info('unfollow')
    router.unfollow(event)


@handler.add(JoinEvent)
def handle_join(event):
    logger.info('join')
    router.join(event)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    logger.info('recieve text message')
    router.textMessage(event)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    logger.info('recieve image message')
    router.imageMessage(event)


@handler.add(PostbackEvent)
def handle_postback(event):
    logger.info('recieve postback message')
    router.postback(event)


if __name__ == "__main__":
    app.run()
