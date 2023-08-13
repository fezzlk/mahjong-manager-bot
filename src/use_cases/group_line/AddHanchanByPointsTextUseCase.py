from DomainService import (
    user_service,
    match_service,
    group_service,
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
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                'グループが登録されていません。招待し直してください。'
            )
            return
        active_match = match_service.find_one_by_id(group.active_match_id)
        if active_match is None:
            active_match = match_service.create_with_line_group_id(line_group_id)
            group.active_match_id = active_match._id
            group_service.update(group)
        
        new_hanchan = Hanchan(
            line_group_id=line_group_id,
            raw_scores=points,
            converted_scores=[],
            match_id=active_match._id,
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
