"""message"""

import re
import random
import datetime

KANSUJI = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
HAI = [k+'萬' for k in KANSUJI] + [k+'筒' for k in KANSUJI] + \
    [k+'索' for k in KANSUJI] + ['白', '發', '中', '東', '南', '西', '北']


class MessageService:
    """message service"""

    # def __init__(self):

    def get_random_hai(self):
        now = datetime.datetime.now()
        random.seed(int(now.year+now.month+now.day) +
                    int(re.sub("\\D", "", self.req_user_id)))

        return random.choice(HAI)
