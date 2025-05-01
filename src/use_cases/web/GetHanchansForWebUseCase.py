from typing import List

from DomainModel.entities.Hanchan import Hanchan
from repositories import hanchan_repository, session_scope


class GetHanchansForWebUseCase:

    def execute(self) -> List[Hanchan]:
        with session_scope() as session:
            return hanchan_repository.find(session=session)
