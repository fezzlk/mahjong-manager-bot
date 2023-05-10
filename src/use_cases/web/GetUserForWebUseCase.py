from repositories import (
    user_repository, session_scope
)
from DomainModel.entities.User import User


class GetUserForWebUseCase:

    def execute(self, id) -> User:
        with session_scope() as session:
            records = user_repository.find(session, [_id])
            if len(records) > 0:
                return records[0]
            else:
                None
