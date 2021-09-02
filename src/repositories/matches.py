
"""
matches repository
"""

from models import Matches
from sqlalchemy import and_


class MatchesRepository:

    def find_by_ids(session, ids):
        # 配列をサニタイズ
        if type(ids) != list:
            ids = [ids]

        return session\
            .query(Matches)\
            .filter(Matches.id.in_([int(s) for s in ids]))\
            .order_by(Matches.id)\
            .all()

    def find_by_room_id_and_status(session, room_id, status):
        return session\
            .query(Matches).filter(and_(
                Matches.room_id == room_id,
                Matches.status == status,
            )).order_by(Matches.id.desc())\
            .first()

    def find_many_by_room_id_and_status(session, room_id, status):
        return session\
            .query(Matches).filter(and_(
                Matches.room_id == room_id,
                Matches.status == status,
            )).order_by(Matches.id.desc())\
            .all()

    def create(session, room_id):
        match = Matches(room_id=room_id)
        session.add(match)

    def find_all(session):
        return session\
            .query(Matches)\
            .order_by(Matches.id)\
            .all()
