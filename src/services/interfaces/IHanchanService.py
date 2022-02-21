from abc import ABCMeta, abstractmethod
from typing import Dict, List, Tuple
from domains.entities.Hanchan import Hanchan
from domains.entities.Match import Match


class IHanchanService(metaclass=ABCMeta):

    @abstractmethod
    def add_or_drop_raw_score(
        self,
        line_group_id: str,
        line_user_id: str,
        raw_score: int,
    ) -> Hanchan:
        pass

    @abstractmethod
    def update_converted_score(
        self,
        line_group_id: str,
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
    def update_status_active_hanchan(
        self,
        line_group_id: str,
        status: int,
    ) -> Hanchan:
        pass

    @abstractmethod
    def archive(self, line_group_id: str) -> Hanchan:
        pass

    @abstractmethod
    def disable(self, line_group_id: str) -> Hanchan:
        pass

    @abstractmethod
    def create(
        self,
        raw_scores: Dict[str, int],
        line_group_id: str,
        related_match: Match,
    ) -> Hanchan:
        pass

    @abstractmethod
    def get(self, ids: List = None) -> List[Hanchan]:
        pass

    @abstractmethod
    def delete(self, ids: List[int]) -> List[Hanchan]:
        pass

    @abstractmethod
    def run_calculate(
        self,
        points: Dict[str, int],
        ranking_prize: List[int],
        tobi_prize: int = 0,
        rounding_method: str = None,
        tobashita_player_id: str = None,
    ) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_point_and_name_from_text(
        self,
        text: str,
    ) -> Tuple[str, str]:
        pass
