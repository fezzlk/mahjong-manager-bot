"""app"""

import os
import re
import random
import datetime
from linebot import LineBotApi

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)

KANSUJI = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
HAI = [k+'萬' for k in KANSUJI] + [k+'筒' for k in KANSUJI] + \
    [k+'索' for k in KANSUJI] + ['白', '發', '中', '東', '南', '西', '北']


class AppService:
    """app service"""

    def __init__(self, service, logger):
        self.line_bot_api = line_bot_api
        self.logger = logger
        self.req_user_id = None
        self.req_room_id = None
        self.db = None

    def set_db(self, db):
        self.db = db

    def set_req_info(self, event):
        """set request info"""

        self.req_user_id = event.source.user_id
        if event.source.type == 'room':
            self.req_room_id = event.source.room_id

    def delete_req_info(self):
        """delete request info"""

        self.req_user_id = None
        self.req_room_id = None

    def get_random_hai(self):
        now = datetime.datetime.now()
        random.seed(int(now.year+now.month+now.day) +
                    int(re.sub("\\D", "", self.req_user_id)))

        return random.choice(HAI)
