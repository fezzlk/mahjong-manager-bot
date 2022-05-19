from DomainService import (
    user_service,
    hanchan_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import (
    session_scope,
    yakuman_user_repository,
    user_repository,
)
from DomainModel.entities.YakumanUser import YakumanUser

from use_cases.group_line.CalculateUseCase import CalculateUseCase


class AddPointByTextUseCase:

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

        point_with_yakuman = point[:]
        point = point.replace('役', '')

        if not point.isdigit():
            reply_service.add_message(
                '点数は整数で入力してください。',
            )
            return None

        if isMinus:
            point = '-' + point

        hanchan = hanchan_service.add_or_drop_raw_score(
            line_group_id=line_group_id,
            line_user_id=target_line_user_id,
            raw_score=int(point),
        )

        points = hanchan.raw_scores

        res = []
        is_contain_not_friend = False
        for line_user_id, point in points.items():
            user_name = user_service.get_name_by_line_user_id(line_user_id)
            if user_name is None:
                is_contain_not_friend = True
                continue
            res.append(
                f'{user_name}: {point}'
            )

        if is_contain_not_friend:
            reply_service.add_message('友達登録しているユーザーのみ表示します。')

        reply_service.add_message("\n".join(res))

        with session_scope() as session:
            target_user = user_repository.find_one_by_line_user_id(
                session, target_line_user_id)
            for _ in range(len(point_with_yakuman) - len(point)):
                yakuman_user_repository.create(session, YakumanUser(
                    user_id=target_user._id,
                    hanchan_id=hanchan._id,
                ))

        reply_service.add_message("\n".join('役満おめでとうございます！'))

        if len(points) == 4:
            CalculateUseCase().execute()
        elif len(points) > 4:
            reply_service.add_message(
                '5人以上入力されています。@[ユーザー名] で不要な入力を消してください。'
            )

        return
