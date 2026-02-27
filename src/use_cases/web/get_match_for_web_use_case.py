from typing import Optional

from domain_model.entities.match import Match
from repositories import match_repository

from .web_utils import find_one_by_id


class GetMatchForWebUseCase:

    def execute(self, _id) -> Optional[Match]:
        return find_one_by_id(match_repository, _id)
