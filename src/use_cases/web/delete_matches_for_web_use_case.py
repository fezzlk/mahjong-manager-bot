from typing import List

from repositories import match_repository

from .web_utils import delete_by_ids


class DeleteMatchesForWebUseCase:

    def execute(self, target_ids: List[int]) -> None:
        delete_by_ids(match_repository, target_ids)
