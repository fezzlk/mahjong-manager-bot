from models import MatchSchema
from sqlalchemy import and_
from domains.Match import Match
from sqlalchemy.orm.session import Session as BaseSession
import json


class MatchRepository:

    def find_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> list:
        records = session\
            .query(MatchSchema)\
            .filter(MatchSchema.id.in_([int(s) for s in ids]))\
            .order_by(MatchSchema.id)\
            .all()

        return [
            Match(
                _id=record.id,
                line_group_id=record.line_group_id,
                hanchan_ids=json.loads(record.hanchan_ids),
                users=record.users,
                status=record.status,
                created_at=record.created_at,
            )
            for record in records
        ]

    def find_one_by_line_group_id_and_status(
        self,
        session: BaseSession,
        line_group_id: str,
        status: int,
    ) -> Match:
        record = session\
            .query(MatchSchema).filter(and_(
                MatchSchema.line_group_id == line_group_id,
                MatchSchema.status == status,
            )).order_by(MatchSchema.id.desc())\
            .first()

        if record is None:
            return None

        return Match(
            _id=record.id,
            line_group_id=record.line_group_id,
            hanchan_ids=json.loads(record.hanchan_ids),
            users=record.users,
            status=record.status,
            created_at=record.created_at,
        )

    def find_many_by_group_id_and_status(
        self,
        session: BaseSession,
        line_group_id: str,
        status: int
    ) -> list:
        records = session\
            .query(MatchSchema).filter(and_(
                MatchSchema.line_group_id == line_group_id,
                MatchSchema.status == status,
            )).order_by(MatchSchema.id.desc())\
            .all()

        return [
            Match(
                _id=record.id,
                line_group_id=record.line_group_id,
                hanchan_ids=json.loads(record.hanchan_ids),
                users=record.users,
                status=record.status,
                created_at=record.created_at,
            )
            for record in records
        ]

    def create(
        self,
        session: BaseSession,
        new_match: Match,
    ) -> None:
        record = MatchSchema(
            line_group_id=new_match.line_group_id,
            hanchan_ids=new_match.hanchan_ids,
            status=new_match.status,
        )

        session.add(record)

    def find_all(
        self,
        session: BaseSession,
    ) -> list:
        records = session\
            .query(MatchSchema)\
            .order_by(MatchSchema.id)\
            .all()

        return [
            Match(
                _id=record.id,
                line_group_id=record.line_group_id,
                hanchan_ids=json.loads(record.hanchan_ids),
                users=record.users,
                status=record.status,
                created_at=record.created_at,
            )
            for record in records
        ]

    def add_hanchan_id_by_line_group_id(
        self,
        session: BaseSession,
        line_group_id: str,
        hanchan_id: int,
    ) -> Match:
        record = session\
            .query(MatchSchema).filter(and_(
                MatchSchema.line_group_id == line_group_id,
                MatchSchema.status == 1,
            )).order_by(MatchSchema.id.desc())\
            .first()

        if record is None:
            return None

        hanchan_ids = json.loads(record.hanchan_ids)
        hanchan_ids.append(str(hanchan_id))
        record.hanchan_ids = json.dumps(list(set(hanchan_ids)))

        return Match(
            _id=record.id,
            line_group_id=record.line_group_id,
            hanchan_ids=hanchan_ids,
            users=record.users,
            status=record.status,
            created_at=record.created_at,
        )

    def update_one_status_by_line_group_id(
        self,
        session: BaseSession,
        line_group_id: str,
        status: int,
    ) -> Match:
        record = session\
            .query(MatchSchema).filter(and_(
                MatchSchema.line_group_id == line_group_id,
                MatchSchema.status == 1,
            )).order_by(MatchSchema.id.desc())\
            .first()

        if record is None:
            return None

        record.status = status

        return Match(
            _id=record.id,
            line_group_id=record.line_group_id,
            hanchan_ids=json.loads(record.hanchan_ids),
            users=record.users,
            status=record.status,
            created_at=record.created_at,
        )

    def update_one_hanchan_ids_by_line_group_id(
        self,
        session: BaseSession,
        line_group_id: str,
        hanchan_ids: list,
    ) -> Match:
        record = session\
            .query(MatchSchema).filter(and_(
                MatchSchema.line_group_id == line_group_id,
                MatchSchema.status == 1,
            )).order_by(MatchSchema.id.desc())\
            .first()

        if record is None:
            return None

        record.hanchan_ids = json.dumps(hanchan_ids)

        return Match(
            _id=record.id,
            line_group_id=record.line_group_id,
            hanchan_ids=json.loads(record.hanchan_ids),
            users=record.users,
            status=record.status,
            created_at=record.created_at,
        )

    def remove_hanchan_id_by_id(
        self,
        session: BaseSession,
        match_id: int,
        hanchan_id: int,
    ) -> Match:
        record = session\
            .query(MatchSchema).filter(and_(
                MatchSchema.id == match_id,
            )).order_by(MatchSchema.id.desc())\
            .first()

        if record is None:
            return None

        hanchan_ids = json.loads(record.hanchan_ids)
        if hanchan_id in hanchan_ids:
            hanchan_ids.remove(hanchan_id)
        record.hanchan_ids = json.dumps(hanchan_ids)

        return Match(
            _id=record.id,
            line_group_id=record.line_group_id,
            hanchan_ids=json.loads(record.hanchan_ids),
            users=record.users,
            status=record.status,
            created_at=record.created_at,
        )
