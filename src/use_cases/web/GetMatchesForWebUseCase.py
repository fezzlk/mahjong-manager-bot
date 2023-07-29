from typing import List
from DomainModel.entities.Match import Match
from repositories import session_scope, match_repository


class GetMatchesForWebUseCase:

    def execute(self) -> List[Match]:
        with session_scope() as session:
            return match_repository.find(session=session)
