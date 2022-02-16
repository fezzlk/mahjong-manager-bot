from typing import List
from Repositories import (
    user_repository, session_scope
)
from Domains.Entities.User import User


class GetUsersForWebUseCase:

    def execute(self) -> List[User]:
        with session_scope() as session:
            return user_repository.find_all(session)
