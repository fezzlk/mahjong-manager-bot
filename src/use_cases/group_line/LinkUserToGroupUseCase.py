from ApplicationService import (
    request_info_service,
    reply_service,
)
from DomainModel.entities.UserGroup import UserGroup

from repositories import (
    session_scope,
    user_group_repository,
)


class LinkUserToGroupUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        line_user_id = request_info_service.req_line_user_id
        with session_scope() as session:
            user_group = user_group_repository.find_one(
                session=session,
                line_group_id=line_group_id,
                line_user_id=line_user_id,
            )

            if user_group is None:
                user_group_repository.create(
                    session=session, new_user_group=UserGroup(
                        line_group_id=line_group_id,
                        line_user_id=line_user_id,
                    )
                )
                reply_service.add_message('このグループの参加メンバーとして登録しました。')
            else:
                reply_service.add_message('すでにこのグループの参加メンバーとして登録されています。')
