from typing import List
from services import (
    match_service,
)
from domains.Match import Match


class GetMatchesForWebUseCase:

    def execute(self) -> List[Match]:
        match_service.get()
