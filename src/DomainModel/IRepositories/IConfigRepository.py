from abc import ABCMeta, abstractmethod
from typing import List
from DomainModel.entities.Config import Config
from sqlalchemy.orm.session import Session as BaseSession


class IConfigRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_config: Config,
    ) -> Config:
        pass

    @abstractmethod
    def delete_by_ids(
        self,
        session: BaseSession,
        ids: List[int],
    ) -> int:
        pass

    @abstractmethod
    def delete_by_target_id_and_key(
        self,
        session: BaseSession,
        target_id: str,
        key: str,
    ) -> int:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> List[Config]:
        pass

    @abstractmethod
    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> List[Config]:
        pass

    @abstractmethod
    def find_by_target_id(
        self,
        session: BaseSession,
        target_id: str,
    ) -> Config:
        pass

    @abstractmethod
    def find_one_by_target_id_and_key(
        self,
        session: BaseSession,
        target_id: str,
        key: str,
    ) -> Config:
        pass
