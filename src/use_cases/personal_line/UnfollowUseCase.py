from ApplicationService import (
    request_info_service,
)
from repositories import (
    user_repository, session_scope
)


class UnfollowUseCase:

    def execute(self) -> None:
        """unfollow event"""
        with session_scope() as session:
            user_repository.delete_by_line_user_id(
                session=session,
                line_user_id=request_info_service.req_line_user_id,
            )
