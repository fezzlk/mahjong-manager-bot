from abc import ABCMeta, abstractmethod


class ICalculateService(metaclass=ABCMeta):
    @abstractmethod
    def run_calculate(
        self,
        points: dict,
        ranking_prize: list,
        tobi_prize: int = 0,
        rounding_method: str = None,
        tobashita_player_id: str = None,
    ) -> dict:
        pass
