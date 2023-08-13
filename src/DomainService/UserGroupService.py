"""user"""

from .interfaces.IUserGroupService import IUserGroupService
from DomainModel.entities.UserGroup import UserGroup
from repositories import user_group_repository
from typing import List


class UserGroupService(IUserGroupService):

    def find_all_by_line_group_id(self, line_group_id: str) -> List[UserGroup]:
        return user_group_repository.find(query={'line_group_id': line_group_id})
