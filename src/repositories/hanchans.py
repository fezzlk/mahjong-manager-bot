
"""
hanchans repository
"""

from models import Hanchans
from sqlalchemy import and_, desc


class HanchansRepository:

    def find_by_id_and_room_id(session, target_id, room_id):
        return session\
            .query(Hanchans)\
            .filter(and_(
                Hanchans.room_id == room_id,
                Hanchans.id == target_id,
            ))\
            .first()

    def find_by_room_id_and_status(session, room_id, status):
        return session\
            .query(Hanchans).filter(and_(
                Hanchans.room_id == room_id,
                Hanchans.status == 1,
            ))\
            .order_by(desc(Hanchans.id))\
            .first()

    def find_by_ids(session, ids):
        # 配列をサニタイズ
        if type(ids) != list:
            ids = [ids]

        # TODO use map to filter
        return session\
            .query(Hanchans)\
            .filter(Hanchans.id.in_([int(s) for s in ids]))\
            .order_by(Hanchans.id)\
            .all()

    def find_all(session):
        return session\
            .query(Hanchans)\
            .order_by(Hanchans.id)\
            .all()

    def create(session, room_id, match_id, raw_scores):
        hanchan = Hanchans(
            room_id=room_id,
            match_id=match_id,
            raw_scores=raw_scores,
        )
        session.add(hanchan)
        return hanchan

    def delete_by_ids(session, ids):
        # 配列をサニタイズ
        if type(ids) != list:
            ids = [ids]
