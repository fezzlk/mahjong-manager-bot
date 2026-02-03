from typing import List

from domain_model.entities.match import Match
from repositories import match_repository, session_scope


class GetMatchesForWebUseCase:

    def execute(self) -> List[Match]:
        with session_scope() as session:
            return match_repository.find(session=session)
