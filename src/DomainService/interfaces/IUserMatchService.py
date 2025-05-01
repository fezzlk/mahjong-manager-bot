from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List

from bson.objectid import ObjectId

from DomainModel.entities.UserMatch import UserMatch


class IUserMatchService(metaclass=ABCMeta):

    @abstractmethod
    def find_all_by_user_id_list(
        self,
        user_ids: List[ObjectId],
        from_dt: datetime = None,
        to_dt: datetime = None,
    ) -> List[UserMatch]:
        pass
