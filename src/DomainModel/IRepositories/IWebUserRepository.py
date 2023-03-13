from abc import ABCMeta, abstractmethod
from typing import List
from DomainModel.entities.WebUser import WebUser
from sqlalchemy.orm.session import Session as BaseSession


class IWebUserRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_webuser: WebUser,
    ) -> WebUser:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> List[WebUser]:
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
    ) -> WebUser:
        pass

    @abstractmethod
    def update(
        self,
        session: BaseSession,
        target: WebUser,
    ) -> int:
        pass
