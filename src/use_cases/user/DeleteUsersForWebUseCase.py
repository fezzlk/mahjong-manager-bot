from typing import List
from services import (
    user_service,
)


class DeleteUsersForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        user_service.delete(ids)
