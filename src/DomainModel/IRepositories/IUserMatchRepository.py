from abc import ABCMeta, abstractmethod
from typing import List, Dict
from DomainModel.entities.UserMatch import UserMatch


class IUserMatchRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_record: UserMatch,
    ) -> UserMatch:
        pass

    @abstractmethod
    def find(
        self,
        query: Dict[str, any] = {},
    ) -> List[UserMatch]:
        pass

    @abstractmethod
    def delete(
        self,
        query: Dict[str, any] = {},
    ) -> int:
        pass
