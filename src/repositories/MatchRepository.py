
"""
matches repository
"""

from models import Matches
from sqlalchemy import and_
from domains.Match import Match
import json


class MatchRepository:

    def find_by_ids(self, session, ids):
        # 配列をサニタイズ
        if type(ids) != list:
            ids = [ids]

        records = session\
            .query(Matches)\
            .filter(Matches.id.in_([int(s) for s in ids]))\
            .order_by(Matches.id)\
            .all()

        return [
            Match(
                _id=record.id,
                line_room_id=record.room_id,
                hanchan_ids=json.loads(record.result_ids),
                users=record.users,
                status=record.status,
                created_at=record.created_at,
            )
            for record in records
        ]

    def find_one_by_line_room_id_and_status(
        self,
        session,
        line_room_id,
        status,
    ):
        record = session\
            .query(Matches).filter(and_(
                Matches.room_id == line_room_id,
                Matches.status == status,
            )).order_by(Matches.id.desc())\
            .first()

        if record is None:
            return None

        return Match(
            _id=record.id,
            line_room_id=record.room_id,
            hanchan_ids=json.loads(record.result_ids),
            users=record.users,
            status=record.status,
            created_at=record.created_at,
        )

    def find_many_by_room_id_and_status(self, session, line_room_id, status):
        records = session\
            .query(Matches).filter(and_(
                Matches.room_id == line_room_id,
                Matches.status == status,
            )).order_by(Matches.id.desc())\
            .all()

        return [
            Match(
                _id=record.id,
                line_room_id=record.room_id,
                hanchan_ids=json.loads(record.result_ids),
                users=record.users,
                status=record.status,
                created_at=record.created_at,
            )
            for record in records
        ]

    def create(self, session, new_match):
        record = Matches(
            line_room_id=new_match.line_room_id,
            hanchan_ids=json.dumps(new_match.hanchan_ids),
            status=new_match.status,
        )

        session.add(record)

    def find_all(self, session):
        records = session\
            .query(Matches)\
            .order_by(Matches.id)\
            .all()

        return [
            Match(
                _id=record.id,
                line_room_id=record.room_id,
                hanchan_ids=json.loads(record.result_ids),
                users=record.users,
                status=record.status,
                created_at=record.created_at,
            )
            for record in records
        ]

    def add_hanchan_id_by_line_room_id(
        self,
        session,
        line_room_id,
        hanchan_id,
    ):
        record = session\
            .query(Matches).filter(and_(
                Matches.room_id == line_room_id,
                Matches.status == 1,
            )).order_by(Matches.id.desc())\
            .first()

        if record is None:
            return None

        hanchan_ids = json.loads(record.result_ids)
        hanchan_ids.append(str(hanchan_id))
        record.result_ids = json.dumps(list(set(hanchan_ids)))

        return Match(
            _id=record.id,
            line_room_id=record.room_id,
            hanchan_ids=hanchan_ids,
            users=record.users,
            status=record.status,
            created_at=record.created_at,
        )

    def update_one_status_by_line_room_id(
        self,
        session,
        line_room_id,
        status,
    ):
        record = session\
            .query(Matches).filter(and_(
                Matches.room_id == line_room_id,
                Matches.status == 1,
            )).order_by(Matches.id.desc())\
            .first()

        if record is None:
            return None

        record.status = status

        return Match(
            _id=record.id,
            line_room_id=record.room_id,
            hanchan_ids=json.loads(record.result_ids),
            users=record.users,
            status=record.status,
            created_at=record.created_at,
        )

    def update_one_hanchan_ids_by_line_room_id(
        self,
        session,
        line_room_id,
        hanchan_ids,
    ):
        record = session\
            .query(Matches).filter(and_(
                Matches.room_id == line_room_id,
                Matches.status == 1,
            )).order_by(Matches.id.desc())\
            .first()

        if record is None:
            return None

        record.hanchan_ids = json.dumps(hanchan_ids)

        return Match(
            _id=record.id,
            line_room_id=record.room_id,
            hanchan_ids=json.loads(record.result_ids),
            users=record.users,
            status=record.status,
            created_at=record.created_at,
        )

    def remove_hanchan_id_by_id(
        self,
        session,
        match_id,
        hanchan_id,
    ):
        record = session\
            .query(Matches).filter(and_(
                Matches.id == match_id,
            )).order_by(Matches.id.desc())\
            .first()

        if record is None:
            return None

        hanchan_ids = json.loads(record.result_ids)
        if hanchan_id in hanchan_ids:
            hanchan_ids.remove(hanchan_id)
        record.hanchan_ids = json.dumps(hanchan_ids)

        return Match(
            _id=record.id,
            line_room_id=record.room_id,
            hanchan_ids=json.loads(record.result_ids),
            users=record.users,
            status=record.status,
            created_at=record.created_at,
        )
