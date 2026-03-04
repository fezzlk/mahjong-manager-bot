import logging

from application_service import (
    request_info_service,
)
from repositories import (
    user_repository,
)

logger = logging.getLogger(__name__)


class UnfollowUseCase:

    def execute(self) -> None:
        """Unfollow event"""
        line_user_id = request_info_service.req_line_user_id
        logger.info("unfollow: user=%s", line_user_id)
        user_repository.delete(
            query={
                "line_user_id": line_user_id,
            },
        )
