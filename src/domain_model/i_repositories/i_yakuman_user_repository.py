from abc import ABCMeta, abstractmethod
from typing import Dict, List, Tuple

from pymongo import ASCENDING

from domain_model.entities.yakuman_user import YakumanUser


class IYakumanUserRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_record: YakumanUser,
    ) -> YakumanUser:
        pass

    @abstractmethod
    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        pass

    @abstractmethod
    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [("_id", ASCENDING)],
    ) -> List[YakumanUser]:
        pass

    @abstractmethod
    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        pass
