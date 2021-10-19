from abc import ABCMeta, abstractmethod
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
