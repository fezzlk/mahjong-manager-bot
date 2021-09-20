# flake8: noqa: E999
"""point"""

import json
from services import (
    app_service,
    hanchans_service,
    reply_service,
    user_service,
    points_service,
)


class PointsUseCases:
    """point use cases"""

    def reply(self, result=None):
        """reply"""

        if result is None:
            room_id = app_service.req_room_id
            result = hanchans_service.get_current(room_id)
        points = json.loads(result.points)
        if len(points) == 0:
            reply_service.add_message(
                '点数を入力してください。「@{ユーザー名} {点数}」でユーザーを指定して入力することもできます。')
            return
        res = [
            f'{user_service.get_name_by_line_user_id(user_id)}: {point}' for user_id, point in points.items()
        ]
        reply_service.add_message("\n".join(res))

    def add_by_text(self, text):
        if text[0] == '@':
            point, target_user = points_service.get_point_and_name_from_text(
                text[1:]
            )
            target_line_user_id = user_service.get_user_id_by_name(
                target_user
            )

            if point == 'delete':
                points = hanchans_service.drop_point(
                    target_line_user_id)
                return points
        else:
            target_line_user_id = app_service.req_user_line_id
            point = text

        point = point.replace(',', '')

        # 入力した点数のバリデート（hack: '-' を含む場合数値として判断できないため一旦エスケープ）
        isMinus = False
        if point[0] == '-':
            point = point[1:]
            isMinus = True

        if not point.isdigit():
            reply_service.add_message(
                '点数は整数で入力してください。（中断したい場合は _exit)')
            return None

        if isMinus:
            point = '-' + point

        points = hanchans_service.add_point(
            target_line_user_id,
            int(point),
        )

        return points
