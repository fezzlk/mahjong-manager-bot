from abc import ABCMeta, abstractmethod
from typing import List
from Entities.User import User, UserMode
from sqlalchemy.orm.session import Session as BaseSession


class IUserRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_user: User,
    ) -> User:
        pass

    @abstractmethod
    def delete_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> int:
        pass

    @abstractmethod
    def delete_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
    ) -> int:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> List[User]:
        pass

    @abstractmethod
    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> List[User]:
        pass

    @abstractmethod
    def find_one_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
    ) -> User:
        pass

    @abstractmethod
    def find_one_by_name(
        self,
        session: BaseSession,
        line_user_name: str,
    ) -> User:
        pass

    @abstractmethod
    def update_one_mode_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
        mode: UserMode,
    ) -> User:
        pass

    @abstractmethod
    def update_one_zoom_url_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
        zoom_url: str,
    ) -> User:
        pass
