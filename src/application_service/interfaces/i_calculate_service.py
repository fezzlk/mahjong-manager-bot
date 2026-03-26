from abc import ABCMeta, abstractmethod
from typing import Dict, List


class ICalculateService(metaclass=ABCMeta):

    @abstractmethod
    def run(
        self,
        points: Dict[str, int],
        ranking_prize: List[int],
        tobi_prize: int = 0,
        rounding_method: str = None,
        tobashita_player_id: str = None,
    ) -> Dict[str, int]:
        pass
