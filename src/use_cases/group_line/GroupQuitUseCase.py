from DomainModel.entities.Group import GroupMode
from DomainService import (
    group_service,
)
from ApplicationService import (
    request_info_service,
)


class GroupQuitUseCase:

    def execute(self) -> None:
        group_service.delete_by_line_group_id(request_info_service.req_line_group_id)
