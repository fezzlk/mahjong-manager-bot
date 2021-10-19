import re
import random
import datetime

KANSUJI = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
HAI = [k + '萬' for k in KANSUJI] + [k + '筒' for k in KANSUJI] + \
    [k + '索' for k in KANSUJI] + ['白', '發', '中', '東', '南', '西', '北']

wait_messages = [
    '雑談してる暇があったら麻雀の勉強をしましょう。',
    '自己分析が大事です。',
    '今日は七対子を積極的に狙いましょう。',
    'まずは平和・断么九',
    '今日は役満が出そうです！（誰がとは言いませんが）',
    '攻めて攻めて攻めまくりましょう！',
    '裏目ってもめげない姿勢！',
    'まもなく天和が訪れるでしょう。',
    '積極的に槓しましょう！',
    '積極的に鳴きましょう！',
    'テンパイ即リー',
]

finish_hanchan_messages = [
    '今回の結果に一喜一憂せず次の戦いに望んでください。',
    '次の半荘で役満が出る予感...',
    '今回の反省点を次に活かしましょう',
    'エンターテイメント性を重視しましょう！'
]


class MessageService:

    def get_random_hai(
        self,
        user_id: str,
    ) -> str:
        now = datetime.datetime.now()
        random.seed(
            int(now.year + now.month + now.day) +
            int(re.sub("\\D", "", user_id))
        )

        return random.choice(HAI)

    def get_wait_massage(self) -> str:
        return random.choice(wait_messages)

    def get_finish_hanchan_message(self) -> str:
        return random.choice(finish_hanchan_messages)
