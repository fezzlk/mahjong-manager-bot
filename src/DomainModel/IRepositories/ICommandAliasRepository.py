from abc import ABCMeta, abstractmethod
from typing import Dict, List, Tuple

from pymongo import ASCENDING

from DomainModel.entities.CommandAlias import CommandAlias


class ICommandAliasRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_record: CommandAlias,
    ) -> CommandAlias:
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
    ) -> List[CommandAlias]:
        pass

    @abstractmethod
    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        pass
