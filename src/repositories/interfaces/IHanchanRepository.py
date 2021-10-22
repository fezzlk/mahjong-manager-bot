from abc import ABCMeta, abstractmethod
from domains.Hanchan import Hanchan
from sqlalchemy.orm.session import Session as BaseSession


class IHanchanRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_one_by_id_and_line_room_id(
        self,
        session: BaseSession,
        target_id: str,
        line_room_id: str,
    ) -> Hanchan:
        pass

    @abstractmethod
    def find_one_by_line_room_id_and_status(
        self,
        session: BaseSession,
        line_room_id: str,
        status: int,
    ) -> Hanchan:
        pass

    @abstractmethod
    def find_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> list:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> list:
        pass

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_hanchan: Hanchan,
    ) -> None:
        pass

    @abstractmethod
    def delete_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> None:
        pass

    @abstractmethod
    def update_raw_score_of_user_by_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        line_user_id: str,
        raw_score: int = None,
    ) -> Hanchan:
        pass

    @abstractmethod
    def update_status_by_line_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        status: int,
    ) -> Hanchan:
        pass

    @abstractmethod
    def update_status_by_id_and_line_room_id(
        self,
        session: BaseSession,
        hanchan_id: int,
        line_room_id: str,
        status: int,
    ) -> Hanchan:
        pass

    @abstractmethod
    def update_one_converted_score_by_line_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        converted_scores: dict,
    ) -> Hanchan:
        pass
