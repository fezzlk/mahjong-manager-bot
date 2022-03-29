from repositories import (
    user_repository, session_scope
)
from DomainModel.entities.User import User


class GetUserForWebUseCase:

    def execute(self, _id) -> User:
        with session_scope() as session:
            users = user_repository.find_by_ids(session, [_id])
            if len(users) > 0:
                return users[0]
            else:
                None
