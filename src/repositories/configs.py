"""
configs repository
"""

from models import Configs
from sqlalchemy import and_


class ConfigsRepository:

    def find(session, target_id, key):
        return session\
            .query(Configs)\
            .filter(and_(
                Configs.target_id == target_id,
                Configs.key == key,
            ))\
            .first()

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

    def create(session, target_id, key, value):
        config = Configs(
            target_id=target_id,
            key=key,
            value=value,
        )
        session.add(config)

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
