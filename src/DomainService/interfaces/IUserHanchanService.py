from abc import ABCMeta, abstractmethod
from DomainModel.entities.UserHanchan import UserHanchan
from typing import List


class IUserHanchanService(metaclass=ABCMeta):

    @abstractmethod
    def find_all_each_line_user_id(self, line_user_ids: List[str]) -> List[UserHanchan]:
        pass
