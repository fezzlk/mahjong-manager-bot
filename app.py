"""application root"""

import set_local_env  # for dev

from db_setting import Engine
from models import Base, Users

import os
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
from sqlalchemy import *
# from migrate import *
from router import Router
from services import Services

# テーブルの作成
Base.metadata.create_all(bind=Engine)

YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

app = Flask(__name__)
logger = logging.create_logger(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)

services = Services()
services.app_service.set_db(db)
router = Router(services)


@app.route('/')
def hello_world():
    Base.metadata.drop_all(bind=Engine)
    Base.metadata.create_all(bind=Engine)
    return "hello world."


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except exceptions.InvalidSignatureError:
        abort(400)
    return 'OK'

# handle event


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
    # port = int(os.getenv("PORT"))
    # app.run(host="0.0.0.0", port=port)
