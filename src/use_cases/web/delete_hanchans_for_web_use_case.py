from typing import List

from repositories import hanchan_repository

from .web_utils import delete_by_ids


class DeleteHanchansForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        delete_by_ids(hanchan_repository, ids)
