"""
rooms repository
"""

from models import Rooms
from domains.room import Room, RoomMode


class RoomRepository:

    def find_one_by_room_id(session, room_id):
        record = session\
            .query(Rooms)\
            .filter(Rooms.room_id == room_id)\
            .first()

        if record is None:
            return None

        return Room(
            line_room_id=record.room_id,
            zoom_url=record.zoom_url,
            mode=RoomMode[record.mode],
            _id=record.id,
        )

    def find_by_ids(session, ids):
        # 配列にサニタイズ
        if type(ids) != list:
            ids = [ids]

        records = session\
            .query(Rooms)\
            .filter(Rooms.id.in_(ids))\
            .order_by(Rooms.id)\
            .all()

        return [
            Room(
                line_room_id=record.room_id,
                zoom_url=record.zoom_url,
                mode=RoomMode[record.mode],
                _id=record.id,
            )
            for record in records
        ]

    def find_all(session):
        records = session\
            .query(Rooms)\
            .order_by(Rooms.id)\
            .all()

        return [
            Room(
                line_room_id=record.room_id,
                zoom_url=record.zoom_url,
                mode=RoomMode[record.mode],
                _id=record.id,
            )
            for record in records
        ]

    def create(session, new_room):
        record = Rooms(
            room_id=new_room.line_room_id,
            mode=new_room.mode.value,
            zoom_url=new_room.zoom_url,
        )
        session.add(record)

    def delete_by_ids(session, ids):
        # 配列をサニタイズ
        if type(ids) != list:
            ids = [ids]

        session\
            .query(Rooms)\
            .filter(Rooms.id.in_(ids))\
            .delete(synchronize_session=False)
