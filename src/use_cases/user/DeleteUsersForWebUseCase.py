from typing import List
from services import (
    user_service,
)


class DeleteUsersForWebUseCase:

    def execute(self, ids: List[int]):
        user_service.delete(ids)
