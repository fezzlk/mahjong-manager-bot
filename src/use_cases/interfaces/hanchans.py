from abc import ABC, abstractmethod


class IHanchansUseCases(ABC):

    @abstractmethod
    def create_and_calculate_from_text_rows(self, text_rows: List[str]):
        pass

    @abstractmethod
    def add_points(self, points: dict}):
        pass
