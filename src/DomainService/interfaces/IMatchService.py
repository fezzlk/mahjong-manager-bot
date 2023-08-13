from typing import Optional
from abc import ABCMeta, abstractmethod
from DomainModel.entities.Match import Match


class IMatchService(metaclass=ABCMeta):

    # @abstractmethod
    # def add_hanchan_id(
    #     self,
    #     line_group_id: str,
    #     hanchan_id: int,
    # ) -> Match:
    #     pass

    # @abstractmethod
    # def remove_hanchan_id(
    #     self,
    #     match_id: int,
    #     hanchan_id: int,
    # ) -> Match:
    #     pass

    @abstractmethod
    def add_or_drop_tip_score(
        self,
        line_group_id: str,
        line_user_id: str,
        tip_score: Optional[int],
    ) -> Match:
        pass
