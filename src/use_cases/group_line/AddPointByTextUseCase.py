from DomainService import (
    user_service,
    hanchan_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from use_cases.group_line.CalculateUseCase import CalculateUseCase


class AddPointByTextUseCase:

    def execute(
        self,
        text: str,
    ) -> None:
        line_group_id = request_info_service.req_line_group_id

        if text[0] == '@':
            point, target_user = hanchan_service.get_point_and_name_from_text(
                text[1:]
            )
            target_line_user_id = user_service.get_line_user_id_by_name(
                target_user
            )

            if point == 'delete':
                hanchan = hanchan_service.add_or_drop_raw_score(
                    line_group_id,
                    target_line_user_id,
                    raw_score=None,
                )

                res = [
                    f'{user_service.get_name_by_line_user_id(line_user_id)}: {point}'
                    for line_user_id, point in hanchan.raw_scores.items()
                ]

                if len(res) == 0:
                    reply_service.add_message("点数を入力してください")
                else:
                    reply_service.add_message("\n".join(res))

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

        yakuman_line_user_ids = [target_line_user_id] * point.count('+')
        if len(yakuman_line_user_ids):
            hanchan_service.create_yakuman_users_to_current(
                line_group_id=line_group_id,
                yakuman_line_user_ids=yakuman_line_user_ids,
            )
            reply_service.add_message(
                "役満おめでとうございます！\nよければどの役満を出したのかチャットで送ってください！")

        point = point.replace('+', '')

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

        res = [
            f'{user_service.get_name_by_line_user_id(line_user_id)}: {point}'
            for line_user_id, point in points.items()
        ]

        reply_service.add_message("\n".join(res))

        if len(points) == 4:
            CalculateUseCase().execute()
        elif len(points) > 4:
            reply_service.add_message(
                '5人以上入力されています。@[ユーザー名] で不要な入力を消してください。'
            )

        return
