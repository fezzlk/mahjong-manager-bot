"""
config repository
"""

from models import Configs
from domains.config import Config
from sqlalchemy import and_


class ConfigRepository:

    def find_one_by_target_id_and_key(session, target_id, key):
        if target_id is None or key is None:
            raise ValueError(
                'Invalid args error: target_id and key are not None'
            )

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

    def find_all(session):
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

    def find_by_target_id(session, target_id):
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

    def find_by_ids(session, ids):
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

    def create(session, config):
        record = Configs(
            target_id=config.target_id,
            key=config.key,
            value=config.value,
        )
        session.add(record)

    def delete_by_target_id_and_key(session, target_id, key):
        if target_id is None or key is None:
            raise ValueError(
                'Invalid args error: target_id and key are not None'
            )

        session\
            .query(Configs)\
            .filter(and_(
                Configs.target_id == target_id,
                Configs.key == key,
            ))\
            .delete()

    def delete_by_ids(session, ids):
        # 配列にサニタイズ
        if type(ids) != list:
            ids = [ids]

        session\
            .query(Configs)\
            .filter(Configs.id.in_(ids))\
            .delete(synchronize_session=False)
