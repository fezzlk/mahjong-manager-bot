"""
rooms repository
"""

from models import Rooms


class RoomsRepository:

    def find_by_room_id(session, room_id):
        return session\
            .query(Rooms)\
            .filter(Rooms.room_id == room_id)\
            .first()

    def find_by_ids(session, ids):
        # 配列にサニタイズ
        if type(ids) != list:
            ids = [ids]

        return session\
            .query(Rooms)\
            .filter(Rooms.id.in_(ids))\
            .order_by(Rooms.id)\
            .all()

    def find_all(session):
        return session\
            .query(Rooms)\
            .order_by(Rooms.id)\
            .all()

    def create(session, room_id, mode):
        room = Rooms(
            room_id=room_id,
            mode=mode,
        )
        session.add(room)
        return room

    def delete_by_ids(session, ids):
        # 配列をサニタイズ
        if type(ids) != list:
            ids = [ids]

        session\
            .query(Rooms)\
            .filter(Rooms.id.in_(ids))\
            .delete(synchronize_session=False)
