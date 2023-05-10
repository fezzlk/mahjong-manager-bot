from typing import List
from repositories import (
    group_repository, session_scope
)
from DomainModel.entities.Group import Group


class GetGroupsForWebUseCase:

    def execute(self) -> List[Group]:
        with session_scope() as session:
            return group_repository.find(session)
