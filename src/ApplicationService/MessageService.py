import re
import random
from datetime import datetime
from DomainModel.entities.Match import Match
from DomainService import (
    user_service,
)
from .interfaces.IMessageService import IMessageService
from typing import Dict, Tuple


KANSUJI = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
HAI = [k + '萬' for k in KANSUJI] + [k + '筒' for k in KANSUJI] + [k + '索' for k in KANSUJI] + ['白', '發', '中', '東', '南', '西', '北']

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


class MessageService(IMessageService):

    def get_random_hai(
        self,
        line_user_id: str,
    ) -> str:
        now = datetime.now()
        random.seed(
            int(now.year + now.month + now.day) + int(re.sub("\\D", "", line_user_id))
        )

        return random.choice(HAI)

    def get_wait_massage(self) -> str:
        return random.choice(wait_messages)

    def get_finish_hanchan_message(self) -> str:
        return random.choice(finish_hanchan_messages)

    def create_show_match_result(self, match: Match) -> str:
        sum_prices_with_tip = match.sum_prices_with_tip
        tip_scores = match.tip_scores
        sum_scores = match.sum_scores

        show_prize_money_list = []
        for line_user_id, score in sum_scores.items():
            name = user_service.get_name_by_line_user_id(line_user_id) or "友達未登録"
            show_score = ("+" if score > 0 else "") + str(score)
            price = sum_prices_with_tip.get(line_user_id, 0)
            tip_count = tip_scores.get(line_user_id, 0)
            additional_tip_message = f'({("+" if tip_count > 0 else "") + str(tip_count)}枚)'

            show_prize_money_list.append(
                f'{name}: {str(price)}円 ({show_score}{additional_tip_message})')
        return '\n'.join(show_prize_money_list)

    def create_show_converted_scores(self, converted_scores: Dict[str, int], sum_scores: Dict[str, int] = None) -> str:
        score_text_list = []
        for r in sorted(
            converted_scores.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            name = user_service.get_name_by_line_user_id(r[0]) or "友達未登録"
            str_score = ("+" if r[1] > 0 else "") + str(r[1])
            if sum_scores is None:
                score_text_list.append(
                    f'{name}: {str_score}'
                )
            else:
                sum_score = sum_scores[r[0]] if r[0] in sum_scores else r[1]
                str_sum_score = ("+" if sum_score > 0 else "") + str(sum_score)
                score_text_list.append(
                    f'{name}: {str_score} ({str_sum_score})'
                )

        return '\n'.join(score_text_list)

    def parse_date_from_text(self, date_str: str) -> Tuple[datetime, bool]:
        # 戻り値の二つ目はis invalid。正常に変換できた場合はFalse、フォーマット不正がある場合はTrueを返す。
        result = None

        if date_str is not None:
            try:
                if not date_str.isdecimal():
                    return (None, True)
                if len(date_str) % 2 == 1:
                    date_str = '0' + date_str

                if len(date_str) == 8:
                    year = int(date_str[:4])
                    month = int(date_str[-4:-2])
                    day = int(date_str[-2:])
                elif len(date_str) == 6:
                    year = 2000 + int(date_str[:2])
                    month = int(date_str[-4:-2])
                    day = int(date_str[-2:])
                elif len(date_str) == 4:
                    year = datetime.now().year
                    month = int(date_str[-4:-2])
                    day = int(date_str[-2:])
                elif len(date_str) == 2:
                    year = datetime.now().year
                    month = datetime.now().month
                    day = int(date_str[-2:])
                else:
                    return (None, True)
                result = datetime(year, month, day)
            except:
                return (None, True)

        return (result, False)

    def create_range_message(self, from_dt: datetime, to_dt: datetime) -> str:
        range_message = ''
        if from_dt is not None:
            range_message += f'{from_dt.strftime("%Y年%m月%d日")}0時から'
        if to_dt is not None:
            range_message += f'{to_dt.strftime("%Y年%m月%d日")}0時まで'

        if range_message == '':
            range_message = None
        else:
            range_message = '範囲指定: ' + range_message
        return range_message
