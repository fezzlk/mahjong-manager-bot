from abc import ABC, abstractmethod


class IPointsUseCases(ABC):

    @abstractmethod
    def add_by_text(self, text: str):
        pass
