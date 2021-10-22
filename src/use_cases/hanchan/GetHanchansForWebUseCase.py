from typing import List
from services import (
    hanchan_service,
)
from domains.Hanchan import Hanchan


class GetHanchansForWebUseCase:

    def execute(self) -> List[Hanchan]:
        return hanchan_service.get()