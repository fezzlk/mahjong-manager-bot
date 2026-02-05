from typing import Optional

from domain_model.entities.match import Match
from repositories import match_repository

from .web_utils import to_object_id


class GetMatchForWebUseCase:

    def execute(self, _id) -> Optional[Match]:
        records = match_repository.find({"_id": to_object_id(_id)})
        return records[0] if len(records) > 0 else None
