from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List

from bson.objectid import ObjectId

from DomainModel.entities.UserHanchan import UserHanchan


class IUserHanchanService(metaclass=ABCMeta):

    @abstractmethod
    def find_all_each_line_user_id(
        self,
        line_user_ids: List[str],
        from_dt: datetime = None,
        to_dt: datetime = None,
    ) -> List[UserHanchan]:
        pass

    @abstractmethod
    def find_all_with_line_user_ids_and_hanchan_ids(
        self,
        line_user_ids: List[str],
        hanchan_ids: List[ObjectId],
        from_dt: datetime = None,
        to_dt: datetime = None,
    ) -> List[UserHanchan]:
        pass
