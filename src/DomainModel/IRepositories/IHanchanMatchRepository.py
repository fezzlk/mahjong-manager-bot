from abc import ABCMeta, abstractmethod
from typing import List, Dict
from DomainModel.entities.HanchanMatch import HanchanMatch


class IHanchanMatchRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_record: HanchanMatch,
    ) -> HanchanMatch:
        pass

    @abstractmethod
    def find(
        self,
        query: Dict[str, any] = {},
    ) -> List[HanchanMatch]:
        pass

    @abstractmethod
    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        pass
