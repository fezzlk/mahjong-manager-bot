from abc import ABCMeta, abstractmethod
from typing import Dict


class IOcrService(metaclass=ABCMeta):
    @abstractmethod
    def is_result_image(self) -> bool:
        pass

    @abstractmethod
    def run(self, content: str = None) -> None:
        pass

    @abstractmethod
    def delete_result(self) -> None:
        pass

    @abstractmethod
    def get_points(self) -> Dict[str, int]:
        pass
