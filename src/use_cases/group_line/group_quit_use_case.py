import logging

from application_service import (
    request_info_service,
)
from domain_service import (
    group_service,
)

logger = logging.getLogger(__name__)


class GroupQuitUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        logger.info("group quit: group=%s", line_group_id)
        group_service.delete_by_line_group_id(line_group_id)
