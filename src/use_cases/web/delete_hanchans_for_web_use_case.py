from typing import List

from repositories import hanchan_repository

from .web_utils import normalize_ids


class DeleteHanchansForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        hanchan_repository.delete({"_id": {"$in": normalize_ids(ids)}})
