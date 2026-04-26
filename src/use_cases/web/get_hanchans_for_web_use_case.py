from typing import List

from domain_model.entities.hanchan import Hanchan
from repositories import hanchan_repository


class GetHanchansForWebUseCase:

    def execute(self) -> List[Hanchan]:
        return hanchan_repository.find()
