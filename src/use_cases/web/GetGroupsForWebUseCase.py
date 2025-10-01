from typing import List

from DomainModel.entities.Group import Group
from repositories import group_repository, session_scope


class GetGroupsForWebUseCase:

    def execute(self) -> List[Group]:
        with session_scope() as session:
            return group_repository.find(session)
