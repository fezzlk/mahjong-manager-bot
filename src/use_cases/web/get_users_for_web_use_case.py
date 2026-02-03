from typing import List

from domain_model.entities.user import User
from repositories import session_scope, user_repository


class GetUsersForWebUseCase:

    def execute(self) -> List[User]:
        with session_scope() as session:
            return user_repository.find(session)
