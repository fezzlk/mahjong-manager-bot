from abc import ABCMeta, abstractmethod
from typing import List, Dict
from DomainModel.entities.UserGroup import UserGroup


class IUserGroupRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_record: UserGroup,
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

    @abstractmethod
    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        pass