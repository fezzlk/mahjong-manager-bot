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
