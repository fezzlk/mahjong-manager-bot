"""root"""

import set_local_env
from setting import Engine
from models import BaseModel, UserModel

import router
import os
from flask import Flask, request, abort, logging, g
from linebot import LineBotApi, WebhookHandler, exceptions
from linebot.models import (
    FollowEvent,
    JoinEvent,
    MessageEvent,
    TextMessage,
    ImageMessage,
    PostbackEvent,
)
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras

from sqlalchemy import Column, String, Integer, create_engine, MetaData, DECIMAL, DATETIME
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = os.environ["DATABASE_URL"]
# Base = declarative_base()
# engine = create_engine(DATABASE_URI,
#                        encoding="utf-8", echo=False)
# metadata = MetaData(engine)
# # create table
# Base.metadata.create_all(engine)


# class User(Base):
#     __tablename__ = "user"
#     __table_args__ = {"mysql_engine": "InnoDB"}
#     id = Column("id", Integer, primary_key=True, autoincrement=True)
#     name = Column("name", String(255))
#     created = Column("created", DATETIME, default=datetime.now, nullable=False)
#     modified = Column("modified", DATETIME,
#                       default=datetime.now, nullable=False)

#     def __init__(self, name):
#         self.name = name
#         now = datetime.now()
#         self.created = now
#         self.modified = now

# テーブルの作成
BaseModel.metadata.create_all(bind=Engine)

# # テーブルの削除
# BaseModel.metadata.drop_all(Engine)

YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

app = Flask(__name__)
logger = logging.create_logger(app)

# DB_NAME = os.environ['DB_NAME']
# DB_USER = os.environ['DB_USER']
# DB_PASSWORD = os.environ['DB_PASSWORD']
# DB_PORT = os.environ['DB_PORT']
# DB_HOST = os.environ['DB_HOST']
# DATABASE_URI = os.environ["DATABASE_URL"]

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)


# # モデル作成
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(80), unique=True)

#     def __init__(self, username, email):
#         self.username = username
#         self.email = email

#     def __repr__(self):
#         return '<User %r>' % self.username


# def get_connection():
#     return psycopg2.connect(
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         port=DB_PORT,
#         host=DB_HOST
#     )


# def get_cursor():
#     with get_connection() as conn:
#         with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
#             return cur


# def create_user_table():
#     with get_cursor() as cur:
#         query = "CREATE TABLE user \
#             (id char(4) not null, \
#             name text not null, \
#             food text not null, \
#             PRIMARY KEY(id));"
#         cur.execute(query)

# def create_user_table():
#     with get_connection() as conn:
#         with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
#             query = "CREATE TABLE USER(\
#                 id char(4) not null,\
#                 name text not null,\
#                 food text not null,\
#                 PRIMARY KEY(id)\
#                 );"
#             cur.execute(query)


@app.route('/')
def hello_world():
    # print(create_user_table())
    user = UserModel(name='name')
    db.session.add(user)
    db.session.commit()
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
