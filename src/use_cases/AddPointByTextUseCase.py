from services import (
    request_info_service,
    reply_service,
    points_service,
    user_service,
    hanchans_service,
)


class AddPointByTextUseCase:

    def execute(self, text):
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
                '点数は整数で入力してください。（中断したい場合は _exit)')
            return None

        if isMinus:
            point = '-' + point

        points = hanchans_service.add_point(
            target_line_user_id,
            int(point),
        )

        return points