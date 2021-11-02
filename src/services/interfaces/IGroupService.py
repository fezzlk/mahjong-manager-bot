from abc import ABCMeta, abstractmethod
from typing import List
from domains.Group import Group, GroupMode


class IGroupService(metaclass=ABCMeta):

    @abstractmethod
    def chmod(
        self,
        line_group_id: str,
        mode: GroupMode,
    ) -> Group:
        pass

    @abstractmethod
    def find_or_create(self, group_id: str) -> Group:
        pass

    @abstractmethod
    def get_mode(self, group_id: str) -> GroupMode:
        pass

    @abstractmethod
    def set_zoom_url(
        self,
        line_group_id: str,
        zoom_url: str,
    ) -> Group:
        pass

    @abstractmethod
    def get_zoom_url(
        self,
        line_group_id: str,
    ) -> str:
        pass

    @abstractmethod
    def get(self, ids: List[int] = None) -> List[Group]:
        pass

    @abstractmethod
    def delete(self, ids: List[int]) -> None:
        pass