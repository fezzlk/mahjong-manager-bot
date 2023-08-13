from DomainModel.entities.Group import GroupMode
from DomainService import (
    group_service,
    match_service,
    hanchan_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)


class ExitUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                'グループが登録されていません。招待し直してください。'
            )
            return
        
        group.mode = GroupMode.wait.value
        group_service.update(group)

        reply_service.add_message(
            '始める時は「_start」と入力してください。')
       
        # group の Active な試合を取得
        active_match = match_service.find_one_by_id(group.active_match_id)

        if active_match is None:
            return
        
        # Active な半荘がある場合は削除
        active_hanchan = hanchan_service.find_one_by_id(active_match.active_hanchan_id)
        active_match.active_hanchan_id = None
        match_service.update(active_match)

        if active_hanchan is None:
            return
        
        active_hanchan.status = 0
        hanchan_service.update(active_hanchan)
