from abc import ABCMeta, abstractmethod
from typing import List, Dict
from DomainModel.entities.UserGroup import UserGroup


class IUserGroupRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_user_group: UserGroup,
    ) -> UserGroup:
        pass

    @abstractmethod
    def find(
        self,
        query: Dict[str, any] = {},
    ) -> List[UserGroup]:
        pass

    @abstractmethod
    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        pass
