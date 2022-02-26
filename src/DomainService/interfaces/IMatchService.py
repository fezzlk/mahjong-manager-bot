from abc import ABCMeta, abstractmethod
from typing import List
from DomainModel.entities.Match import Match


class IMatchService(metaclass=ABCMeta):

    @abstractmethod
    def add_hanchan_id(
        self,
        line_group_id: str,
        hanchan_id: int,
    ) -> Match:
        pass

    @abstractmethod
    def count_results(self, line_group_id: str) -> int:
        pass

    @abstractmethod
    def get_current(self, line_group_id: str) -> Match:
        pass

    @abstractmethod
    def update_status_active_match(
        self,
        line_group_id: str,
        status: int,
    ) -> Match:
        pass

    @abstractmethod
    def archive(self, line_group_id: str) -> Match:
        pass

    @abstractmethod
    def disable(self, line_group_id: str) -> Match:
        pass

    @abstractmethod
    def get_or_create_current(self, line_group_id: str) -> Match:
        pass

    @abstractmethod
    def create(self, line_group_id: str) -> Match:
        pass

    @abstractmethod
    def get_archived(
        self,
        line_group_id: str,
    ) -> List[Match]:
        pass

    @abstractmethod
    def remove_hanchan_id(
        self,
        match_id: int,
        hanchan_id: int,
    ) -> Match:
        pass

    @abstractmethod
    def delete(self, target_ids: List[int]) -> None:
        pass
