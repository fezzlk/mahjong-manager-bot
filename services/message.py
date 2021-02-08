"""message"""

import re
import random
import datetime

KANSUJI = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
HAI = [k+'萬' for k in KANSUJI] + [k+'筒' for k in KANSUJI] + \
    [k+'索' for k in KANSUJI] + ['白', '發', '中', '東', '南', '西', '北']

wait_messages = [
    '雑談してる暇があったら麻雀の勉強をしましょう。',
    '自己分析が大事です。',
    '今日は七対子を積極的に狙いましょう。',
    '配牌がよくない時は平和・断么九',
    '今日は役満が出そうです！（誰がとは言いませんが）',
    '攻めて攻めて攻めまくりましょう！',
    '裏目っちゃうかもです...',
    'まもなく天和が訪れるでしょう。',
]


class MessageService:
    """message service"""

    def __init__(self, services):
        self.services = services

    def get_random_hai(self):
        now = datetime.datetime.now()
        random.seed(
            int(now.year+now.month+now.day) +
            int(re.sub("\\D", "", self.services.app_service.req_user_id))
        )

        return random.choice(HAI)

    def get_wait_massage(self):
        user_id = self.services.app_service.req_user_id
        counter = self.services.user_service()
        now = datetime.datetime.now()
        random.seed(
            int(now.minute) +
            int(re.sub("\\D", "", self.services.app_service.req_user_id))
        )

        return random.choice(wait_messages)
