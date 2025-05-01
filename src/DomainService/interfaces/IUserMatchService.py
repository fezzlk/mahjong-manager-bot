from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Optional

from bson.objectid import ObjectId

from DomainModel.entities.UserMatch import UserMatch


class IUserMatchService(metaclass=ABCMeta):
    @abstractmethod
    def find_all_by_user_id_list(
        self,
        user_ids: List[ObjectId],
        from_dt: Optional[datetime] = None,
        to_dt: Optional[datetime] = None,
    ) -> List[UserMatch]:
        pass
