"""app"""

import os
from linebot import LineBotApi
from flask import logging
from flask_sqlalchemy import SQLAlchemy

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)

# if "YOUR_CHANNEL_ACCESS_TOKEN" in os.environ:
#     YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
#     line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
# else:
#     line_bot_api = None


class AppService:
    """app service"""

    def __init__(self, service, app):
        self.line_bot_api = line_bot_api
        self.logger = logging.create_logger(app)
        self.req_user_id = None
        self.req_room_id = None

        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
        self.db = SQLAlchemy(app)

    def set_req_info(self, event):
        """set request info"""

        self.req_user_id = event.source.user_id
        if event.source.type == 'room':
            self.req_room_id = event.source.room_id

    def delete_req_info(self):
        """delete request info"""

        self.req_user_id = None
        self.req_room_id = None
