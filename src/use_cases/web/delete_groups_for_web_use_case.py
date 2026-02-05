from typing import List

from repositories import group_repository

from .web_utils import normalize_ids


class DeleteGroupsForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        group_repository.delete({"_id": {"$in": normalize_ids(ids)}})
