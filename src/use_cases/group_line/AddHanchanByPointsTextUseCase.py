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
        rows = [r for r in text.split('\n') if ':' in r]
        points = {}
        for r in rows:
            col = r.split(':')
            points[
                user_service.get_line_user_id_by_name(col[0])
            ] = int(col[1])

        line_group_id = request_info_service.req_line_group_id
        current_match = match_service.get_or_create_current(line_group_id)
        hanchan_service.create(points, line_group_id, current_match)

        if len(points) == 4:
            CalculateUseCase().execute()
        else:
            reply_service.add_message(
                '4人分の点数を入力してください'
            )

        return
