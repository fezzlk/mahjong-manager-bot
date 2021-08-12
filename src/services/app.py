"""app"""

import os
from linebot import LineBotApi
from flask import logging
from flask_sqlalchemy import SQLAlchemy


class AppService:
    """
    以下を管理
    - ロガー
    - line bot api インスタンス
    - メッセージ送信元の LINE ユーザー ID, トークルーム ID
    - DB 接続 with SQLAlchemy
    """

    def __init__(self, services, app):
        # logger
        self.logger = logging.create_logger(app)

        # line bot api
        self.line_bot_api = None
        if "YOUR_CHANNEL_ACCESS_TOKEN" in os.environ:
            YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
            self.line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
        else:
            self.logger.warning(
                'line_bot_api is not setup because YOUR_CHANNEL_ACCESS_TOKEN is not found.')

        # 送信元の LINE user ID, LINE room ID
        self.req_user_id = None
        self.req_room_id = None

        # DB 接続
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db = SQLAlchemy(app)

    def set_req_info(self, event):
        """set request infomation from LINE event"""

        self.req_user_id = event.source.user_id
        if event.source.type == 'room':
            self.req_room_id = event.source.room_id

    def delete_req_info(self):
        """
        delete request infomation
        一つ前のメッセージ送信元の情報が残らないようにするために使う
        """

        self.req_user_id = None
        self.req_room_id = None
