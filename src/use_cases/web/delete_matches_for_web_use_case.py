from typing import List

from repositories import match_repository

from .web_utils import normalize_ids


class DeleteMatchesForWebUseCase:

    def execute(self, target_ids: List[int]) -> None:
        match_repository.delete({"_id": {"$in": normalize_ids(target_ids)}})
