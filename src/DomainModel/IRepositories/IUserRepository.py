from abc import ABCMeta, abstractmethod
from typing import Dict, List, Tuple
from DomainModel.entities.User import User
from pymongo import ASCENDING


class IUserRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_record: User,
    ) -> User:
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
    ) -> List[User]:
        pass

    @abstractmethod
    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        pass
