from abc import ABCMeta, abstractmethod
from typing import Dict, List, Tuple
from DomainModel.entities.Hanchan import Hanchan
from pymongo import ASCENDING


class IHanchanRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_record: Hanchan,
    ) -> Hanchan:
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
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[Hanchan]:
        pass

    @abstractmethod
    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        pass
