from typing import List
from .interfaces.IConfigRepository import IConfigRepository
from models import ConfigSchema
from domains.Config import Config
from sqlalchemy import and_
from sqlalchemy.orm.session import Session as BaseSession


class ConfigRepository(IConfigRepository):

    def create(
        self,
        session: BaseSession,
        new_config: Config,
    ) -> None:
        record = ConfigSchema(
            target_id=new_config.target_id,
            key=new_config.key,
            value=new_config.value,
        )
        session.add(record)

    def delete_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> None:
        session\
            .query(ConfigSchema)\
            .filter(ConfigSchema.id.in_(ids))\
            .delete(synchronize_session=False)

    def delete_by_target_id_and_key(
        self,
        session: BaseSession,
        target_id: str,
        key: str,
    ) -> None:
        session\
            .query(ConfigSchema)\
            .filter(and_(
                ConfigSchema.target_id == target_id,
                ConfigSchema.key == key,
            ))\
            .delete()

    def find_all(
        self,
        session: BaseSession,
    ) -> List[Config]:
        records = session\
            .query(ConfigSchema)\
            .order_by(ConfigSchema.id)\
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
        ids: List[str],
    ) -> List[Config]:
        records = session\
            .query(ConfigSchema)\
            .filter(ConfigSchema.id.in_(ids))\
            .order_by(ConfigSchema.id)\
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
            .query(ConfigSchema)\
            .filter(ConfigSchema.target_id == target_id)\
            .order_by(ConfigSchema.id)\
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
            .query(ConfigSchema)\
            .filter(and_(
                ConfigSchema.target_id == target_id,
                ConfigSchema.key == key,
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
