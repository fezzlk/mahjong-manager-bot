from abc import ABCMeta, abstractmethod
from typing import List, Dict
from DomainModel.entities.UserHanchan import UserHanchan


class IUserHanchanRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_record: UserHanchan,
    ) -> UserHanchan:
        pass

    @abstractmethod
    def find(
        self,
        query: Dict[str, any] = {},
    ) -> List[UserHanchan]:
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