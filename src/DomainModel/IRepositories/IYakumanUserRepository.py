from abc import ABCMeta, abstractmethod
from typing import List
from DomainModel.entities.YakumanUser import YakumanUser
from sqlalchemy.orm.session import Session as BaseSession


class IYakumanUserRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_yakuman_user: YakumanUser,
    ) -> YakumanUser:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> List[YakumanUser]:
        pass

    @abstractmethod
    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[int],
    ) -> List[YakumanUser]:
        pass

    @abstractmethod
    def find_by_user_ids(
        self,
        session: BaseSession,
        user_ids: List[str],
    ) -> List[YakumanUser]:
        pass

    @abstractmethod
    def find_by_hanchan_ids(
        self,
        session: BaseSession,
        hanchan_ids: List[str],
    ) -> List[YakumanUser]:
        pass

    @abstractmethod
    def delete_by_ids(
        self,
        session: BaseSession,
        ids: List[int],
    ) -> int:
        pass
