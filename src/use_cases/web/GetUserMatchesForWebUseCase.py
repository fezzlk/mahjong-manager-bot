from typing import List
from repositories import (
    user_match_repository, session_scope
)
from DomainModel.entities.UserMatch import UserMatch


class GetUserMatchesForWebUseCase:

    def execute(self) -> List[UserMatch]:
        with session_scope() as session:
            return user_match_repository.find_all(session)
