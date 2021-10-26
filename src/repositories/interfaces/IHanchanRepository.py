from abc import ABCMeta, abstractmethod
from typing import Dict, List
from domains.Hanchan import Hanchan
from sqlalchemy.orm.session import Session as BaseSession


class IHanchanRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(
        self,
        session: BaseSession,
        new_hanchan: Hanchan,
    ) -> Hanchan:
        pass

    @abstractmethod
    def delete_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> int:
        pass

    @abstractmethod
    def find_all(
        self,
        session: BaseSession,
    ) -> List[Hanchan]:
        pass

    @abstractmethod
    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[Hanchan],
    ) -> List[Hanchan]:
        pass

    @abstractmethod
    def find_one_by_id_and_line_group_id(
        self,
        session: BaseSession,
        target_id: str,
        line_group_id: str,
    ) -> Hanchan:
        pass

    @abstractmethod
    def find_one_by_line_group_id_and_status(
        self,
        session: BaseSession,
        line_group_id: str,
        status: int,
    ) -> Hanchan:
        pass

    @abstractmethod
    def update_one_converted_scores_by_id(
        self,
        session: BaseSession,
        hanchan_id: int,
        converted_scores: Dict[str, int],
    ) -> Hanchan:
        pass

    @abstractmethod
    def update_one_raw_scores_by_id(
        self,
        session: BaseSession,
        hanchan_id: int,
        raw_scores: Dict[str, int],
    ) -> Hanchan:
        pass

    @abstractmethod
    def update_status_by_id(
        self,
        session: BaseSession,
        hanchan_id: int,
        status: int,
    ) -> Hanchan:
        pass
