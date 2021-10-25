from typing import List
from services import (
    group_service,
)


class DeleteGroupsForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        group_service.delete(ids)
