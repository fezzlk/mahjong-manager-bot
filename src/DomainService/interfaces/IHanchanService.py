from abc import ABCMeta, abstractmethod
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

    # @abstractmethod
    # def update_current_converted_score(
    #     self,
    #     line_group_id: str,
    #     converted_scores: Dict[str, int],
    # ) -> Hanchan:
    #     pass

    @abstractmethod
    def update_status_active_hanchan(
        self,
        line_group_id: str,
        status: int,
    ) -> None:
        pass

    @abstractmethod
    def get_current(self, line_group_id: str) -> Hanchan:
        pass
