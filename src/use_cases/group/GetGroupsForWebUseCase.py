from typing import List
from Repositories import (
    group_repository, session_scope
)
from Domains.Entities.Group import Group


class GetGroupsForWebUseCase:

    def execute(self) -> List[Group]:
        with session_scope() as session:
            return group_repository.find_all(session)
