from abc import ABCMeta, abstractmethod
from domains.Room import Room, RoomMode
from sqlalchemy.orm.session import Session as BaseSession


class IRoomRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_one_by_room_id(
        self,
        session: BaseSession,
        room_id: int,
    ) -> Room:
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
        new_room: Room,
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
    def update_one_mode_by_line_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        mode: RoomMode,
    ) -> Room:
        pass

    @abstractmethod
    def update_one_zoom_url_by_line_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        zoom_url: str,
    ) -> Room:
        pass
