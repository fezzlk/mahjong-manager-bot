from typing import List
from services import (
    room_service,
)
from domains.Room import Room


class GetRoomsForWebUseCase:

    def execute(self) -> List[Room]:
        room_service.get()
