from abc import ABCMeta, abstractmethod
from typing import List, Dict, Tuple
from DomainModel.entities.Group import Group
from pymongo import ASCENDING


class IGroupRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_record: Group,
    ) -> Group:
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
        sort: List[Tuple[str, any]] = [('id', ASCENDING)],
    ) -> List[Group]:
        pass

    @abstractmethod
    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        pass
