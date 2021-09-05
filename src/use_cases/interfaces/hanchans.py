from abc import ABC, abstractmethod


class IHanchansUseCases(ABC):

    @abstractmethod
    def add(self, raw_scores: List[str]):
        pass
