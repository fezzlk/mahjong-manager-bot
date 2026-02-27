from typing import List

from repositories import group_setting_repository

from .web_utils import delete_by_ids


class DeleteConfigsForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        delete_by_ids(group_setting_repository, ids)
