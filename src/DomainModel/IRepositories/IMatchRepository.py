from abc import ABCMeta, abstractmethod
from typing import List
from DomainModel.entities.Match import Match
from sqlalchemy.orm.session import Session as BaseSession


class IMatchRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_match: Match,
    ) -> Match:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> List[Match]:
        pass

    @abstractmethod
    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[Match],
    ) -> List[Match]:
        pass

    @abstractmethod
    def find_many_by_line_group_id_and_status(
        self,
        session: BaseSession,
        line_group_id: str,
        status: int
    ) -> List[Match]:
        pass

    @abstractmethod
    def find_one_by_line_group_id_and_status(
        self,
        session: BaseSession,
        line_group_id: str,
        status: int,
    ) -> Match:
        pass

    @abstractmethod
    def update_one_hanchan_ids_by_id(
        self,
        session: BaseSession,
        line_group_id: str,
        hanchan_id: int,
    ) -> Match:
        pass

    @abstractmethod
    def update_one_status_by_id(
        self,
        session: BaseSession,
        line_group_id: str,
        status: int,
    ) -> Match:
        pass

    @abstractmethod
    def delete_by_ids(
        self,
        session: BaseSession,
        ids: List[int],
    ) -> int:
        pass
