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
