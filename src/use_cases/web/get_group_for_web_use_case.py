from typing import Optional

from domain_model.entities.group import Group
from repositories import group_repository

from .web_utils import find_one_by_id


class GetGroupForWebUseCase:

    def execute(self, _id) -> Optional[Group]:
        return find_one_by_id(group_repository, _id)
