from typing import List
from repositories import (
    yakuman_user_repository, session_scope
)
from DomainModel.entities.YakumanUser import YakumanUser


class GetYakumanUsersForWebUseCase:

    def execute(self) -> List[YakumanUser]:
        with session_scope() as session:
            return yakuman_user_repository.find_all(session)
