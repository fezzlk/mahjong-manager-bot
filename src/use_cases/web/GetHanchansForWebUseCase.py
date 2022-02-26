from typing import List
from DomainService import (
    hanchan_service,
)
from DomainModel.entities.Hanchan import Hanchan


class GetHanchansForWebUseCase:

    def execute(self) -> List[Hanchan]:
        return hanchan_service.get()
