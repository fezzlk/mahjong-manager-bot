from abc import ABCMeta, abstractmethod
from domains.User import User, UserMode
from sqlalchemy.orm.session import Session as BaseSession


class IUserRepository(metaclass=ABCMeta):
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
        name: str,
    ) -> User:
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
        new_user: User,
    ) -> None:
        pass

    @abstractmethod
    def delete_one_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
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
    def update_one_mode_by_line_room_id(
        self,
        session: BaseSession,
        line_user_id: str,
        mode: UserMode,
    ) -> User:
        pass

    @abstractmethod
    def update_one_zoom_id_by_line_room_id(
        self,
        session: BaseSession,
        line_user_id: str,
        zoom_url: str,
    ) -> User:
        pass
