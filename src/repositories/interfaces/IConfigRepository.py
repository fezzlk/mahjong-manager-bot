from abc import ABCMeta, abstractmethod
from domains.Config import Config
from sqlalchemy.orm.session import Session as BaseSession


class IConfigRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_one_by_target_id_and_key(
        self,
        session: BaseSession,
        target_id: str,
        key: str,
    ) -> Config:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> list:
        pass

    @abstractmethod
    def find_by_target_id(
        self,
        session: BaseSession,
        target_id: str,
    ) -> Config:
        pass

    @abstractmethod
    def find_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> list:
        pass

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_config: Config,
    ) -> None:
        pass

    @abstractmethod
    def delete_by_target_id_and_key(
        self,
        session: BaseSession,
        target_id: str,
        key: str,
    ) -> None:
        pass

    @abstractmethod
    def delete_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> None:
        pass
