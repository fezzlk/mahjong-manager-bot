from typing import List
from services import (
    room_service,
)


class DeleteRoomsForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        room_service.delete(ids)
