
"""
matches repository
"""

from models import Matches
from sqlalchemy import and_
from domains.Match import Match
import json


class MatchRepository:

    def find_by_ids(session, ids):
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
                line_room_id=record.room_id,
                hanchan_ids=json.loads(record.result_ids),
                users=record.users,
                status=record.status,
                created_at=record.created_at,
            )
            for record in records
        ]

    def find_one_by_line_room_id_and_status(session, line_room_id, status):
        if line_room_id is None or status is None:
            raise ValueError

        record = session\
            .query(Matches).filter(and_(
                Matches.room_id == line_room_id,
                Matches.status == status,
            )).order_by(Matches.id.desc())\
            .first()

        if record is None:
            return None

        return Match(
            line_room_id=record.room_id,
            hanchan_ids=json.loads(record.result_ids),
            users=record.users,
            status=record.status,
            created_at=record.created_at,
        )

    def find_many_by_room_id_and_status(session, line_room_id, status):
        if line_room_id is None or status is None:
            raise ValueError

        records = session\
            .query(Matches).filter(and_(
                Matches.room_id == line_room_id,
                Matches.status == status,
            )).order_by(Matches.id.desc())\
            .all()

        return [
            Match(
                line_room_id=record.room_id,
                result_ids=json.loads(record.result_ids),
                users=record.users,
                status=record.status,
                created_at=record.created_at,
            )
            for record in records
        ]

    def create(session, new_match):
        record = Matches(
            line_room_id=new_match.line_room_id,
            hanchan_ids=json.dumps(new_match.hanchan_ids),
            status=new_match.status,
        )

        session.add(record)

    def find_all(session):
        records = session\
            .query(Matches)\
            .order_by(Matches.id)\
            .all()

        return [
            Match(
                line_room_id=record.room_id,
                hanchan_ids=json.loads(record.result_ids),
                users=record.users,
                status=record.status,
                created_at=record.created_at,
            )
            for record in records
        ]
