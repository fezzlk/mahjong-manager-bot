from abc import ABCMeta, abstractmethod
from domains.Group import Group, GroupMode
from sqlalchemy.orm.session import Session as BaseSession


class IGroupRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_one_by_group_id(
        self,
        session: BaseSession,
        group_id: int,
    ) -> Group:
        pass

    @abstractmethod
    def find_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> list:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> list:
        pass

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_group: Group,
    ) -> None:
        pass

    @abstractmethod
    def delete_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> None:
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
