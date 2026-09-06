from abc import ABCMeta, abstractmethod
from typing import List

from domain_model.entities.guest import Guest


class IGuestService(metaclass=ABCMeta):
    @abstractmethod
    def register_next(self, line_group_id: str) -> Guest:
        pass

    @abstractmethod
    def list_by_group(self, line_group_id: str) -> List[Guest]:
        pass

    @abstractmethod
    def remove(self, line_group_id: str, guest_number: int) -> bool:
        pass
