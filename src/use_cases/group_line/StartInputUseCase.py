from DomainService import (
    group_service,
    match_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import hanchan_repository
from DomainModel.entities.Group import GroupMode
from DomainModel.entities.Hanchan import Hanchan


class StartInputUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id

        mode = group_service.get_mode(line_group_id)
        if mode is None:
            reply_service.add_message('トークルームが登録されていません。招待し直してください。')
            return
        if mode == GroupMode.input:
            reply_service.add_message('すでに入力モードです。')
            return

        current_match = match_service.find_or_create_current(line_group_id)
        new_hanchan = Hanchan(
            line_group_id=line_group_id,
            raw_scores={},
            converted_scores={},
            match_id=current_match._id,
            status=1,
        )
        hanchans = hanchan_repository.find({
            'match_id': current_match._id,
            'status': 2,
        })
        hanchan_repository.create(new_hanchan)

        group_service.chmod(
            line_group_id,
            GroupMode.input,
        )
        reply_service.add_message(
            f'第{len(hanchans)+1}回戦お疲れ様です。各自点数を入力してください。\n（同点の場合は上家が高くなるように数点追加してください）')
