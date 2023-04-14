from abc import ABCMeta, abstractmethod
from typing import List
from DomainModel.entities.UserGroup import UserGroup
from sqlalchemy.orm.session import Session as BaseSession


class IUserGroupRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_user_group: UserGroup,
    ) -> UserGroup:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> List[UserGroup]:
        pass

    @abstractmethod
    def find_by_line_group_id(
        self,
        session: BaseSession,
        line_group_id: str
    ) -> List[UserGroup]:
        pass

    @abstractmethod
    def find_one(
        self,
        session: BaseSession,
        line_group_id: str,
        line_user_id: str,
    ) -> UserGroup:
        pass
