from abc import ABCMeta, abstractmethod
from domains.Match import Match


class IMatchService(metaclass=ABCMeta):

    @abstractmethod
    def add_hanchan_id(
        self,
        line_room_id: str,
        hanchan_id: int,
    ) -> Match:
        pass

    @abstractmethod
    def count_results(self, line_room_id: str) -> int:
        pass

    @abstractmethod
    def get_current(self, line_room_id: str) -> Match:
        pass

    @abstractmethod
    def update_status(
        self,
        line_room_id: str,
        status: int,
    ) -> Match:
        pass

    @abstractmethod
    def archive(self, line_room_id: str) -> Match:
        pass

    @abstractmethod
    def disable(self, line_room_id: str) -> Match:
        pass

    @abstractmethod
    def get_or_create_current(self, line_room_id: str) -> Match:
        pass

    @abstractmethod
    def create(self, line_room_id: str) -> Match:
        pass
