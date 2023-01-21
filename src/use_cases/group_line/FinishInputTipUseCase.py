from DomainModel.entities.Group import GroupMode
from DomainService import (
    group_service,
)
from ApplicationService import (
    request_info_service,
)
from use_cases.group_line.MatchFinishUseCase import MatchFinishUseCase


class FinishInputTipUseCase:

    def execute(self) -> None:
        group_service.chmod(request_info_service.req_line_group_id, GroupMode)
        MatchFinishUseCase().execute()
