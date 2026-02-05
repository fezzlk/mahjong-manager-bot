from typing import List

from domain_model.entities.match import Match
from repositories import match_repository


class GetMatchesForWebUseCase:

    def execute(self) -> List[Match]:
        return match_repository.find()
