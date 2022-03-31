from typing import List
from DomainModel.entities.Hanchan import Hanchan
from repositories import session_scope, hanchan_repository


class GetHanchansForWebUseCase:

    def execute(self) -> List[Hanchan]:
        with session_scope() as session:
            return hanchan_repository.find_all(session=session)
