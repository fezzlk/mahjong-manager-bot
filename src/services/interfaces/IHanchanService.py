from abc import ABCMeta, abstractmethod
from typing import Dict, List
from domains.Hanchan import Hanchan
from domains.Match import Match


class IHanchanService(metaclass=ABCMeta):

    @abstractmethod
    def drop_raw_score(
        self,
        line_room_id: str,
        line_user_id: str,
    ) -> Hanchan:
        pass

    @abstractmethod
    def add_raw_score(
        self,
        line_room_id: str,
        line_user_id: str,
        raw_score: int,
    ) -> Hanchan:
        pass

    @abstractmethod
    def update_converted_score(
        self,
        line_room_id: str,
        converted_scores: Dict[str, int],
    ) -> Hanchan:
        pass

    @abstractmethod
    def find_by_ids(
        self,
        ids: List[str],
    ) -> List[Hanchan]:
        pass

    @abstractmethod
    def update_status(
        self,
        line_room_id: str,
        status: int,
    ) -> Hanchan:
        pass

    @abstractmethod
    def archive(self, line_room_id: str) -> Hanchan:
        pass

    @abstractmethod
    def disable(self, line_room_id: str) -> Hanchan:
        pass

    @abstractmethod
    def create(
        self,
        raw_scores: Dict[str, int],
        line_room_id: str,
        related_match: Match,
    ) -> Hanchan:
        pass