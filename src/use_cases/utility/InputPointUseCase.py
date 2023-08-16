from ApplicationService import (
    request_info_service,
    reply_service,
)
from typing import Optional


class InputPointUseCase:

    """
    受け取ったメッセージから点数登録先ユーザと値の取得
    """

    def execute(self, text: str) -> tuple[str, Optional[int]]:
        mention_line_ids = request_info_service.mention_line_ids

        if len(mention_line_ids) > 1:
            reply_service.add_message(
                'メンションは1回につき1人を指定するようにしてください。')
            return (None, None)
        if len(mention_line_ids) == 1 and len(text[1:].split()) >= 2:
            # ユーザー名に空白がある場合を考慮し、最後の要素をポイントとして判断する
            point = text[1:].split()[-1]
            target_line_user_id = mention_line_ids[0]
        else:
            point = text
            target_line_user_id = request_info_service.req_line_user_id

        point = point.replace(',', '')

        # '-' の場合は削除
        if point == '-':
            return (target_line_user_id, None)
        
        # 入力した点数のバリデート（hack: '-' を含む場合数値として判断できないため一旦エスケープ）
        isMinus = False
        if point[0] == '-':
            point = point[1:]
            isMinus = True

        if not point.isdigit():
            reply_service.add_message(
                '整数で入力してください。',
            )
            return (None, None)

        if isMinus:
            point = '-' + point

        return (target_line_user_id, int(point))
