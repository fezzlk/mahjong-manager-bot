"""
config repository
"""

from models import Configs
from domains.Config import Config
from sqlalchemy import and_
from .interfaces.IConfigRepository import IConfigRepository


class ConfigRepository(IConfigRepository):

    def find_one_by_target_id_and_key(self, session, target_id, key):
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

    def find_all(self, session):
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

    def find_by_target_id(self, session, target_id):
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

    def find_by_ids(self, session, ids):
        # 配列にサニタイズ
        if type(ids) != list:
            ids = [ids]

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

    def create(self, session, new_config):
        record = Configs(
            target_id=new_config.target_id,
            key=new_config.key,
            value=new_config.value,
        )
        session.add(record)

    def delete_by_target_id_and_key(self, session, target_id, key):
        session\
            .query(Configs)\
            .filter(and_(
                Configs.target_id == target_id,
                Configs.key == key,
            ))\
            .delete()

    def delete_by_ids(self, session, ids):
        # 配列にサニタイズ
        if type(ids) != list:
            ids = [ids]

        session\
            .query(Configs)\
            .filter(Configs.id.in_(ids))\
            .delete(synchronize_session=False)
