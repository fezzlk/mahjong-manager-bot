from DomainService import (
    user_service,
    hanchan_service,
    match_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from use_cases.group_line.CalculateUseCase import CalculateUseCase


class AddHanchanByPointsTextUseCase:

    def execute(self, text) -> None:
        line_group_id = request_info_service.req_line_group_id
        rows = [r for r in text.split('\n') if ':' in r]
        points = {}
        yakuman_line_user_ids = []
        for r in rows:
            user_name, point = r.split(':')
            line_user_id = user_service.get_line_user_id_by_name(user_name)
            yakuman_line_user_ids.extend([line_user_id] * point.count('+'))
            point = point.replace('+', '')
            points[line_user_id] = int(point)

        if len(yakuman_line_user_ids):
            hanchan_service.create_yakuman_users_to_current(
                line_group_id=line_group_id,
                yakuman_line_user_ids=yakuman_line_user_ids,
            )
            reply_service.add_message(
                "役満おめでとうございます！\nよければどの役満を出したのかチャットで送ってください！")

        current_match = match_service.get_or_create_current(line_group_id)
        hanchan_service.create(points, line_group_id, current_match)

        if len(points) == 4:
            CalculateUseCase().execute()
        else:
            reply_service.add_message(
                '4人分の点数を入力してください'
            )

        return
