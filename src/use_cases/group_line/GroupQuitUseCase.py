from DomainModel.entities.Group import GroupMode
from DomainService import (
    group_service,
    hanchan_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)


class GroupQuitUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        hanchan_service.update_status_active_hanchan(line_group_id, 0)
        group_service.chmod(
            line_group_id,
            GroupMode.wait,
        )
        reply_service.add_message(
            '始める時は「_start」と入力してください。')
