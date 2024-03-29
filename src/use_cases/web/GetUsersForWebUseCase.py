from typing import List
from repositories import (
    user_repository, session_scope
)
from DomainModel.entities.User import User


class GetUsersForWebUseCase:

    def execute(self) -> List[User]:
        with session_scope() as session:
            return user_repository.find(session)
