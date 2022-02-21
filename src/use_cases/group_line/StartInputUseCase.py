from services import (
    request_info_service,
    reply_service,
    group_service,
    hanchan_service,
    match_service,
)
from domains.entities.Group import GroupMode


class StartInputUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id

        if group_service.get_mode(line_group_id) == GroupMode.input:
            reply_service.add_message('すでに入力モードです')
            return

        current_match = match_service.get_or_create_current(line_group_id)
        hanchan_service.create({}, line_group_id, current_match)

        group_service.chmod(
            line_group_id,
            GroupMode.input,
        )
        reply_service.add_message(
            f'第{match_service.count_results(line_group_id)+1}回戦お疲れ様です。各自点数を入力してください。\n（同点の場合は上家が高くなるように数点追加してください）')
