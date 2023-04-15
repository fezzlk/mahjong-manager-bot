from abc import ABCMeta, abstractmethod
from typing import List, Optional
from DomainModel.entities.WebUser import WebUser
from sqlalchemy.orm.session import Session as BaseSession


class IWebUserRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_web_user: WebUser,
    ) -> WebUser:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> List[WebUser]:
        pass

    @abstractmethod
    def find_by_id(
        self,
        session: BaseSession,
        id: str,
    ) -> WebUser:
        pass

    @abstractmethod
    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> List[WebUser]:
        pass

    @abstractmethod
    def find_one_by_email(
        self,
        session: BaseSession,
        email: str,
    ) -> Optional[WebUser]:
        pass

    @abstractmethod
    def approve_line(
        self,
        session: BaseSession,
        id: str,
    ) -> Optional[WebUser]:
        pass

    @abstractmethod
    def reset_line(
        self,
        session: BaseSession,
        id: str,
    ) -> Optional[WebUser]:
        pass

    @abstractmethod
    def update_linked_line_user_id(
        self,
        session: BaseSession,
        id: str,
        line_user_id: str,
    ) -> Optional[WebUser]:
        pass
