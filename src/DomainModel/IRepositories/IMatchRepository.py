from abc import ABCMeta, abstractmethod
from typing import List, Dict, Tuple
from DomainModel.entities.Match import Match
from pymongo import ASCENDING


class IMatchRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_record: Match,
    ) -> Match:
        pass

    @abstractmethod
    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[Match]:
        pass

    @abstractmethod
    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        pass

    @abstractmethod
    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        pass
