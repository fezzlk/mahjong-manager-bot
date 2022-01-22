from typing import List
from Domains.IRepositories.IConfigRepository import IConfigRepository
from models import ConfigSchema
from Domains.Entities.Config import Config
from sqlalchemy import and_
from sqlalchemy.orm.session import Session as BaseSession


class ConfigRepository(IConfigRepository):

    def create(
        self,
        session: BaseSession,
        new_config: Config,
    ) -> Config:
        record = ConfigSchema(
            target_id=new_config.target_id,
            key=new_config.key,
            value=new_config.value,
        )
        session.add(record)
        session.commit()
        new_config._id = record.id
        return new_config

    def delete_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> int:
        delete_count = session\
            .query(ConfigSchema)\
            .filter(ConfigSchema.id.in_(ids))\
            .delete(synchronize_session=False)

        return delete_count

    def delete_by_target_id_and_key(
        self,
        session: BaseSession,
        target_id: str,
        key: str,
    ) -> int:
        delete_count = session\
            .query(ConfigSchema)\
            .filter(and_(
                ConfigSchema.target_id == target_id,
                ConfigSchema.key == key,
            ))\
            .delete()

        return delete_count

    def find_all(
        self,
        session: BaseSession,
    ) -> List[Config]:
        records = session\
            .query(ConfigSchema)\
            .order_by(ConfigSchema.id)\
            .all()

        return [
            self._mapping_record_to_config_domain(record)
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
            self._mapping_record_to_config_domain(record)
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
            self._mapping_record_to_config_domain(record)
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

        return self._mapping_record_to_config_domain(record)

    def _mapping_record_to_config_domain(self, record: ConfigSchema) -> Config:
        return Config(
            target_id=record.target_id,
            key=record.key,
            value=record.value,
            _id=record.id,
        )
