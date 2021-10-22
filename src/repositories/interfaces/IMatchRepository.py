from abc import ABCMeta, abstractmethod
from domains.Match import Match
from sqlalchemy.orm.session import Session as BaseSession


class IMatchRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> list:
        pass

    @abstractmethod
    def find_one_by_line_room_id_and_status(
        self,
        session: BaseSession,
        line_room_id: str,
        status: int,
    ) -> Match:
        pass

    @abstractmethod
    def find_many_by_room_id_and_status(
        self,
        session: BaseSession,
        line_room_id: str,
        status: int
    ) -> list:
        pass

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_match: Match,
    ) -> None:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> list:
        pass

    @abstractmethod
    def add_hanchan_id_by_line_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        hanchan_id: int,
    ) -> Match:
        pass

    @abstractmethod
    def update_one_status_by_line_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        status: int,
    ) -> Match:
        pass

    @abstractmethod
    def update_one_hanchan_ids_by_line_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        hanchan_ids: list,
    ) -> Match:
        pass

    @abstractmethod
    def remove_hanchan_id_by_id(
        self,
        session: BaseSession,
        match_id: int,
        hanchan_id: int,
    ) -> Match:
        pass
