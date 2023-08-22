from abc import ABCMeta, abstractmethod
from DomainModel.entities.UserMatch import UserMatch
from typing import List
from bson.objectid import ObjectId


class IUserMatchService(metaclass=ABCMeta):

    @abstractmethod
    def find_all_by_user_id_list(self, user_ids: List[ObjectId]) -> List[UserMatch]:
        pass
