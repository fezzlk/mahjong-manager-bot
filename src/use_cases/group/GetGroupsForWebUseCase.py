from typing import List
from services import (
    group_service,
)
from domains.Group import Group


class GetGroupsForWebUseCase:

    def execute(self) -> List[Group]:
        return group_service.get()
