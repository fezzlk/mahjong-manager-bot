from DomainService import (
    user_service,
    match_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import hanchan_repository
from DomainModel.entities.Hanchan import Hanchan
from use_cases.group_line.SubmitHanchanUseCase import SubmitHanchanUseCase


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
        current_match = match_service.find_or_create_current(line_group_id)
        new_hanchan = Hanchan(
            line_group_id=line_group_id,
            raw_scores=points,
            converted_scores=[],
            match_id=current_match._id,
            status=1,
        )
        hanchan_repository.create(new_hanchan)
        if len(points) == 4:
            SubmitHanchanUseCase().execute()
        else:
            reply_service.add_message(
                '4人分の点数を入力してください'
            )

        return
