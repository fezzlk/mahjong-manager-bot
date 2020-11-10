import os
import re
import random
from linebot import LineBotApi

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)

KANSUJI = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
HAI = [k+'萬' for k in KANSUJI] + [k+'筒' for k in KANSUJI] + [k+'索' for k in KANSUJI] + ['白', '發', '中', '東', '南', '西', '北']

class AppService:

    def __init__(self):
        self.line_bot_api = line_bot_api
        self.req_user_id = None

    def get_random_hai(self):
        random.seed(int(re.sub("\\D", "", self.req_user_id)))

        return random.choice(HAI)
