from typing import List

from repositories import group_repository

from .web_utils import delete_by_ids


class DeleteGroupsForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        delete_by_ids(group_repository, ids)
