from abc import ABCMeta, abstractmethod
from typing import List
from domains.Room import Room, RoomMode


class IRoomService(metaclass=ABCMeta):

    @abstractmethod
    def chmod(
        self,
        line_room_id: str,
        mode: RoomMode,
    ) -> Room:
        pass

    @abstractmethod
    def find_or_create(self, room_id: str) -> Room:
        pass

    @abstractmethod
    def get_mode(self, room_id: str) -> RoomMode:
        pass

    @abstractmethod
    def set_zoom_url(
        self,
        line_room_id: str,
        zoom_url: str,
    ) -> Room:
        pass

    @abstractmethod
    def get_zoom_url(
        self,
        line_room_id: str,
    ) -> str:
        pass

    @abstractmethod
    def get(self, ids: List[int] = None) -> List[Room]:
        pass

    @abstractmethod
    def delete(self, ids: List[int]) -> None:
        pass
