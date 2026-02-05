from typing import List

from repositories import group_setting_repository

from .web_utils import normalize_ids


class DeleteConfigsForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        group_setting_repository.delete({"_id": {"$in": normalize_ids(ids)}})
