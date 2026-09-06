from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional, Tuple

from pymongo import ASCENDING

from domain_model.entities.guest import Guest


class IGuestRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        new_record: Guest,
    ) -> Guest:
        pass

    @abstractmethod
    def find(
        self,
        query: Dict[str, any] = {},
        sort: List[Tuple[str, any]] = [("_id", ASCENDING)],
        limit: int = 0,
    ) -> List[Guest]:
        pass

    @abstractmethod
    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        pass

    @abstractmethod
    def find_max_guest_number(self, line_group_id: str) -> Optional[int]:
        """is_deletedを問わず、これまでにこのグループで使われた最大のguest_numberを返す。

        番号の再利用(削除後に同じ番号を別人に割り当てること)を防ぐため、
        通常のfind()のis_deletedフィルタを経由せず全件を対象にする。
        """
