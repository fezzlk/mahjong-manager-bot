from abc import ABCMeta, abstractmethod
from typing import List

from DomainModel.entities.UserGroup import UserGroup


class IUserGroupService(metaclass=ABCMeta):

    @abstractmethod
    def find_all_by_line_group_id(self, line_group_id: str) -> List[UserGroup]:
        pass
