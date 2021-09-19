"""
configs repository
"""

from models import Configs
from domains.config import Config
from sqlalchemy import and_


class ConfigRepository:

    def find_one_by_target_id_and_key(session, target_id, key):
        config = session\
            .query(Configs)\
            .filter(and_(
                Configs.target_id == target_id,
                Configs.key == key,
            ))\
            .first()

        return Config(
            config.target_id,
            config.key,
            config.value,
            config.id,
        )

    def find_all(session):
        return session\
            .query(Configs)\
            .order_by(Configs.id)\
            .all()

    def find_by_target_id(session, target_id):
        return session\
            .query(Configs)\
            .filter(Configs.target_id == target_id)\
            .order_by(Configs.id)\
            .all()

    def find_by_ids(session, ids):
        # 配列にサニタイズ
        if type(ids) != list:
            ids = [ids]

        return session\
            .query(Configs)\
            .filter(Configs.id.in_(ids))\
            .order_by(Configs.id)\
            .all()

    def create(session, config):
        record = Configs(
            target_id=config.target_id,
            key=config.key,
            value=config.value,
        )
        session.add(record)

    def delete(session, target_id, key):
        session\
            .query(Configs)\
            .filter(and_(
                Configs.target_id == target_id,
                Configs.key == key,
            ))\
            .delete()

    def delete_by_ids(session, ids):
        session\
            .query(Configs)\
            .filter(Configs.id.in_(ids))\
            .delete(synchronize_session=False)
