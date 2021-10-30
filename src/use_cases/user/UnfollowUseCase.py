from services import (
    request_info_service,
    user_service,
)


class UnfollowUseCase:

    def execute(self) -> None:
        """unfollow event"""
        user_service.delete_by_line_user_id(
            request_info_service.req_line_user_id
        )
