"""
rooms repository
"""

from models import Rooms
from domains.Room import Room, RoomMode
from sqlalchemy.orm.session import Session as BaseSession


class RoomRepository:

    def find_one_by_room_id(
        self,
        session: BaseSession,
        room_id: int,
    ) -> Room:
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

    def find_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> list:
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

    def find_all(
        self,
        session: BaseSession,
    ) -> list:
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

    def create(
        self,
        session: BaseSession,
        new_room: Room,
    ) -> None:
        record = Rooms(
            room_id=new_room.line_room_id,
            mode=new_room.mode.value,
            zoom_url=new_room.zoom_url,
        )
        session.add(record)

    def delete_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> None:
        session\
            .query(Rooms)\
            .filter(Rooms.id.in_(ids))\
            .delete(synchronize_session=False)

    def update_one_mode_by_line_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        mode: RoomMode,
    ) -> Room:
        if line_room_id is None:
            raise ValueError

        record = session\
            .query(Rooms)\
            .filter(Rooms.room_id == line_room_id)\
            .first()

        if record is None:
            return None

        record.mode = mode.value

        return Room(
            line_room_id=record.room_id,
            zoom_url=record.zoom_url,
            mode=RoomMode[record.mode],
            _id=record.id,
        )

    def update_one_zoom_url_by_line_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        zoom_url: str,
    ) -> Room:
        record = session\
            .query(Rooms)\
            .filter(Rooms.room_id == line_room_id)\
            .first()

        if record is None:
            return None

        record.zoom_url = zoom_url

        return Room(
            line_room_id=record.room_id,
            zoom_url=record.zoom_url,
            mode=RoomMode[record.mode],
            _id=record.id,
        )
