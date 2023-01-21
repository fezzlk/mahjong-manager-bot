from DomainService import (
    user_service,
    match_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)


class AddTipByTextUseCase:

    def execute(
        self,
        text: str,
    ) -> None:
        line_group_id = request_info_service.req_line_group_id
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
                ' チップ枚数は整数で入力してください。',
            )
            return None

        if isMinus:
            point = '-' + point

        match = match_service.add_or_drop_tip_score(
            line_group_id=line_group_id,
            line_user_id=target_line_user_id,
            tip_score=int(point),
        )

        tips = match.tip_scores

        res = [
            f'{user_service.get_name_by_line_user_id(line_user_id)}: {chip}'
            for line_user_id, chip in tips.items()
        ]

        reply_service.add_message("\n".join(res))
        return