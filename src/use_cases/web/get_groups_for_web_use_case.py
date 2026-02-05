from typing import List

from domain_model.entities.group import Group
from repositories import group_repository


class GetGroupsForWebUseCase:

    def execute(self) -> List[Group]:
        return group_repository.find()
