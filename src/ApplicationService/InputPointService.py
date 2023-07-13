from ApplicationService import (
    request_info_service,
    reply_service,
)


class InputPointService:
    """InputPointService
        受け取った点数入力メッセージに関する処理
    """

    """
    受け取ったメッセージから登録先ユーザと値の取得
    """

    def extract_point_from_text(self, text: str) -> tuple[int, str]:
        mention_line_ids = request_info_service.mention_line_ids

        if len(mention_line_ids) > 0:
            if len(mention_line_ids) == 1 and len(text[1:].split()) >= 2:
                # ユーザー名に空白がある場合を考慮し、最後の要素をポイントとして判断する
                point = text[1:].split()[-1]
                target_line_user_id = mention_line_ids[0]
            else:
                reply_service.add_message(
                    'ユーザーを指定する場合はメンションをつけてメッセージの末尾に点数を入力してください。1回につき1人を指定するようにしてください。')
                return
        else:
            target_line_user_id = request_info_service.req_line_user_id
            point = text

        point = point.replace(',', '')

        # 入力した点数のバリデート（hack: '-' を含む場合数値として判断できないため一旦エスケープ）
        isMinus = False
        if point[0] == '-':
            point = point[1:]
            isMinus = True

        if not point.isdigit():
            reply_service.add_message(
                '点数は整数で入力してください。',
            )
            return None

        if isMinus:
            point = '-' + point

        return (point, target_line_user_id)
