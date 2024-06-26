from typing import Optional
from abc import ABCMeta, abstractmethod
from DomainModel.entities.Match import Match
from bson.objectid import ObjectId
from typing import List

class IMatchService(metaclass=ABCMeta):

    @abstractmethod
    def add_or_drop_tip_score(
        self,
        line_group_id: str,
        line_user_id: str,
        tip_score: Optional[int],
    ) -> Match:
        pass

    @abstractmethod
    def find_one_by_id(self, _id: ObjectId) -> Optional[Match]:
        pass
    
    @abstractmethod
    def create_with_line_group_id(self, line_group_id: str) -> Match:
        pass

    @abstractmethod
    def update(self, target: Match) -> None:
        pass

    @abstractmethod
    def find_all_for_graph(self, ids: List[ObjectId]) -> List[Match]:
        pass

    @abstractmethod
    def find_all_by_ids_and_line_group_ids(self, ids: List[ObjectId], line_group_ids: List[str]) -> List[Match]:
        pass
    
    @abstractmethod
    def find_latest_one(self, line_group_id: str) -> Optional[Match]:
        pass

    @abstractmethod
    def find_all_archived_by_line_group_id(self, line_group_id: str) -> List[Match]:
        pass
