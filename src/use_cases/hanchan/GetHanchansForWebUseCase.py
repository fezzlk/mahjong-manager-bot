from typing import List
from Services import (
    hanchan_service,
)
from Domains.Entities.Hanchan import Hanchan


class GetHanchansForWebUseCase:

    def execute(self) -> List[Hanchan]:
        return hanchan_service.get()
