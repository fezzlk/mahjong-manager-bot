"""user"""

from typing import List

from domain_model.entities.user_group import UserGroup
from repositories import user_group_repository

from .interfaces.i_user_group_service import IUserGroupService


class UserGroupService(IUserGroupService):

    def find_all_by_line_group_id(self, line_group_id: str) -> List[UserGroup]:
        return user_group_repository.find(query={"line_group_id": line_group_id})
