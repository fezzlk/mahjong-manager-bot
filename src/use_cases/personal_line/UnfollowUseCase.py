from ApplicationService import (
    request_info_service,
)
from repositories import (
    user_repository,
)


class UnfollowUseCase:

    def execute(self) -> None:
        """unfollow event"""
        user_repository.delete(
            query={
                'line_user_id': request_info_service.req_line_user_id,
            }
        )
