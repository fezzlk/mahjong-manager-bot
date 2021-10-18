"""
config repository
"""

from .interfaces.IConfigRepository import IConfigRepository
from models import Configs
from domains.Config import Config
from sqlalchemy import and_
from sqlalchemy.orm.session import Session as BaseSession


class ConfigRepository(IConfigRepository):

    def create(
        self,
        session: BaseSession,
        new_config: Config,
    ) -> None:
        record = Configs(
            target_id=new_config.target_id,
            key=new_config.key,
            value=new_config.value,
        )
        session.add(record)

    def delete_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> None:
        session\
            .query(Configs)\
            .filter(Configs.id.in_(ids))\
            .delete(synchronize_session=False)

    def delete_by_target_id_and_key(
        self,
        session: BaseSession,
        target_id: str,
        key: str,
    ) -> None:
        session\
            .query(Configs)\
            .filter(and_(
                Configs.target_id == target_id,
                Configs.key == key,
            ))\
            .delete()

    def find_all(
        self,
        session: BaseSession,
    ) -> list:
        records = session\
            .query(Configs)\
            .order_by(Configs.id)\
            .all()

        return [
            Config(
                target_id=record.target_id,
                key=record.key,
                value=record.value,
                _id=record.id,
            )
            for record in records
        ]

    def find_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> list:
        records = session\
            .query(Configs)\
            .filter(Configs.id.in_(ids))\
            .order_by(Configs.id)\
            .all()

        return [
            Config(
                target_id=record.target_id,
                key=record.key,
                value=record.value,
                _id=record.id,
            )
            for record in records
        ]

    def find_by_target_id(
        self,
        session: BaseSession,
        target_id: str,
    ) -> Config:
        records = session\
            .query(Configs)\
            .filter(Configs.target_id == target_id)\
            .order_by(Configs.id)\
            .all()

        return [
            Config(
                target_id=record.target_id,
                key=record.key,
                value=record.value,
                _id=record.id,
            )
            for record in records
        ]

    def find_one_by_target_id_and_key(
        self,
        session: BaseSession,
        target_id: str,
        key: str,
    ) -> Config:
        record = session\
            .query(Configs)\
            .filter(and_(
                Configs.target_id == target_id,
                Configs.key == key,
            ))\
            .first()

        if record is None:
            return None

        return Config(
            target_id=record.target_id,
            key=record.key,
            value=record.value,
            _id=record.id,
        )
