from DomainService import (
    match_service,
)
from ApplicationService import (
    request_info_service,
)


class DisableMatchUseCase:

    def execute(self) -> None:
        match_service.disable(request_info_service.req_line_group_id)
