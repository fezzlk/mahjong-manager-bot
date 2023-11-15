from abc import ABCMeta, abstractmethod
from DomainModel.entities.Match import Match
from typing import Dict

class IMessageService(metaclass=ABCMeta):

    @abstractmethod
    def get_random_hai(
        self,
        line_user_id: str,
    ) -> str:
        pass

    @abstractmethod
    def get_wait_massage(self) -> str:
        pass

    @abstractmethod
    def get_finish_hanchan_message(self) -> str:
        pass

    @abstractmethod
    def create_show_match_result(self, match: Match) -> str:
        pass

    @abstractmethod
    def create_show_converted_scores(self, converted_scores: Dict[str, int], sum_scores: Dict[str, int] = None) -> str:
        pass