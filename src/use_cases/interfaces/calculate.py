from abc import ABC, abstractmethod


class ICalculateUseCases(ABC):

    @abstractmethod
    def calculate(self, point: dict, tobashita_player_id=str):
        pass
