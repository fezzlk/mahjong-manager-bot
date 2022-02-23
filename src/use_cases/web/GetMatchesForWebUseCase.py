from typing import List
from services import (
    match_service,
)
from DomainModel.entities.Match import Match


class GetMatchesForWebUseCase:

    def execute(self) -> List[Match]:
        return match_service.get()
