from abc import ABCMeta, abstractmethod
from typing import List, Optional

from bson.objectid import ObjectId

from DomainModel.entities.Hanchan import Hanchan


class IHanchanService(metaclass=ABCMeta):

    @abstractmethod
    def add_or_drop_raw_score(
        self,
        line_group_id: str,
        line_user_id: str,
        raw_score: int,
    ) -> Hanchan:
        pass

    @abstractmethod
    def find_one_by_id(self, _id: ObjectId) -> Optional[Hanchan]:
        pass

    @abstractmethod
    def create_with_line_group_id_and_match_id(self, line_group_id: str, match_id: ObjectId) -> Hanchan:
        pass

    @abstractmethod
    def find_all_archived_by_match_id(self, match_id: ObjectId) -> List[Hanchan]:
        pass

    @abstractmethod
    def find_all_archived_by_match_ids(self, match_ids: List[ObjectId]) -> List[Hanchan]:
        pass

    @abstractmethod
    def update(self, target: Hanchan) -> None:
        pass

    @abstractmethod
    def disable_by_match_id(self, match_id: ObjectId) -> None:
        pass
