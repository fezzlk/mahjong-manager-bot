from abc import ABCMeta, abstractmethod
from typing import List
from DomainModel.entities.UserMatch import UserMatch
from sqlalchemy.orm.session import Session as BaseSession


class IUserMatchRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_user_match: UserMatch,
    ) -> UserMatch:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> List[UserMatch]:
        pass

    @abstractmethod
    def find_by_user_ids(
        self,
        session: BaseSession,
        user_ids: List[str],
    ) -> List[UserMatch]:
        pass

    @abstractmethod
    def find_by_match_id(
        self,
        session: BaseSession,
        match_id: int,
    ) -> List[UserMatch]:
        pass
