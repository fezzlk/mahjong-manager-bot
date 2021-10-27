from abc import ABCMeta, abstractmethod
from typing import List
from domains.Group import Group, GroupMode
from sqlalchemy.orm.session import Session as BaseSession


class IGroupRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_group: Group,
    ) -> Group:
        pass

    @abstractmethod
    def delete_by_ids(
        self,
        session: BaseSession,
        ids: List[Group],
    ) -> int:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> List[Group]:
        pass

    @abstractmethod
    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> List[Group]:
        pass

    @abstractmethod
    def find_one_by_line_group_id(
        self,
        session: BaseSession,
        line_group_id: int,
    ) -> Group:
        pass

    @abstractmethod
    def update_one_mode_by_line_group_id(
        self,
        session: BaseSession,
        line_group_id: str,
        mode: GroupMode,
    ) -> Group:
        pass

    @abstractmethod
    def update_one_zoom_url_by_line_group_id(
        self,
        session: BaseSession,
        line_group_id: str,
        zoom_url: str,
    ) -> Group:
        pass
