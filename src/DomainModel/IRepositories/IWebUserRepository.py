from abc import ABCMeta, abstractmethod
from typing import Dict, List, Tuple
from DomainModel.entities.WebUser import WebUser
from pymongo import ASCENDING


class IWebUserRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_record: WebUser,
    ) -> WebUser:
        pass

    @abstractmethod
    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [('_id', ASCENDING)],
    ) -> List[WebUser]:
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
