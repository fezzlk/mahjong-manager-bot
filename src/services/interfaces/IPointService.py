from abc import ABCMeta, abstractmethod
from typing import Tuple


class IPointService(metaclass=ABCMeta):
    @abstractmethod
    def get_point_and_name_from_text(
        self,
        text: str,
    ) -> Tuple[str, str]:
        pass
