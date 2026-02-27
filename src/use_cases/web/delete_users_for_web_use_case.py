from typing import List

from repositories import user_repository

from .web_utils import delete_by_ids


class DeleteUsersForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        delete_by_ids(user_repository, ids)
