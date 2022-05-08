from typing import List
from DomainModel.IRepositories.IConfigRepository import IConfigRepository
from db_models import ConfigModel
from DomainModel.entities.Config import Config
from sqlalchemy import and_
from sqlalchemy.orm.session import Session as BaseSession


class ConfigRepository(IConfigRepository):

    def create(
        self,
        session: BaseSession,
        new_config: Config,
    ) -> Config:
        record = ConfigModel(
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
        ids: List[int],
    ) -> int:
        delete_count = session\
            .query(ConfigModel)\
            .filter(ConfigModel.id.in_(ids))\
            .delete(synchronize_session=False)

        return delete_count

    def delete_by_target_id_and_key(
        self,
        session: BaseSession,
        target_id: str,
        key: str,
    ) -> int:
        delete_count = session\
            .query(ConfigModel)\
            .filter(and_(
                ConfigModel.target_id == target_id,
                ConfigModel.key == key,
            ))\
            .delete()

        return delete_count

    def find_all(
        self,
        session: BaseSession,
    ) -> List[Config]:
        records = session\
            .query(ConfigModel)\
            .order_by(ConfigModel.id)\
            .all()

        return [
            self._mapping_record_to_domain(record)
            for record in records
        ]

    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> List[Config]:
        records = session\
            .query(ConfigModel)\
            .filter(ConfigModel.id.in_(ids))\
            .order_by(ConfigModel.id)\
            .all()

        return [
            self._mapping_record_to_domain(record)
            for record in records
        ]

    def find_by_target_id(
        self,
        session: BaseSession,
        target_id: str,
    ) -> Config:
        records = session\
            .query(ConfigModel)\
            .filter(ConfigModel.target_id == target_id)\
            .order_by(ConfigModel.id)\
            .all()

        return [
            self._mapping_record_to_domain(record)
            for record in records
        ]

    def find_one_by_target_id_and_key(
        self,
        session: BaseSession,
        target_id: str,
        key: str,
    ) -> Config:
        record = session\
            .query(ConfigModel)\
            .filter(and_(
                ConfigModel.target_id == target_id,
                ConfigModel.key == key,
            ))\
            .first()

        if record is None:
            return None

        return self._mapping_record_to_domain(record)

    def update(
        self,
        session: BaseSession,
        target: Config,
    ) -> int:
        updated = ConfigModel(
            target_id=target.target_id,
            key=target.key,
            value=target.value,
        ).__dict__
        updated.pop('_sa_instance_state')

        result: int = session\
            .query(ConfigModel)\
            .filter(ConfigModel.id == target._id)\
            .update(updated)

        return result

    def _mapping_record_to_domain(self, record: ConfigModel) -> Config:
        return Config(
            target_id=record.target_id,
            key=record.key,
            value=record.value,
            _id=record.id,
        )
