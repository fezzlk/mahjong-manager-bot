from typing import List
from Services import (
    match_service,
)
from Domains.Entities.Match import Match


class GetMatchesForWebUseCase:

    def execute(self) -> List[Match]:
        return match_service.get()
