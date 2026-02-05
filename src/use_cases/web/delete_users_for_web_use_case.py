from typing import List

from repositories import user_repository

from .web_utils import normalize_ids


class DeleteUsersForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        user_repository.delete({"_id": {"$in": normalize_ids(ids)}})
