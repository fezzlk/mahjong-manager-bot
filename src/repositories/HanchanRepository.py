
"""
hanchans repository
"""

from models import Hanchans
from sqlalchemy import and_, desc
from domains.Hanchan import Hanchan
import json


class HanchanRepository:

    def find_one_by_id_and_line_room_id(
        self,
        session,
        target_id,
        line_room_id,
    ):
        if target_id is None or line_room_id is None:
            raise ValueError

        record = session\
            .query(Hanchans)\
            .filter(and_(
                Hanchans.room_id == line_room_id,
                Hanchans.id == target_id,
            ))\
            .first()

        if record is None:
            return None

        return Hanchan(
            line_room_id=record.room_id,
            raw_scores=json.loads(record.raw_scores),
            converted_scores=json.loads(record.converted_scores),
            match_id=record.match_id,
            status=record.status,
        )

    def find_one_by_line_room_id_and_status(
        self,
        session,
        line_room_id,
        status
    ):
        if status is None or line_room_id is None:
            raise ValueError

        record = session\
            .query(Hanchans).filter(and_(
                Hanchans.room_id == line_room_id,
                Hanchans.status == status,
            ))\
            .order_by(desc(Hanchans.id))\
            .first()

        if record is None:
            return None

        return Hanchan(
            line_room_id=record.room_id,
            raw_scores=json.loads(record.raw_scores),
            converted_scores=json.loads(record.converted_scores),
            match_id=record.match_id,
            status=record.status,
        )

    def find_by_ids(self, session, ids):
        # 配列をサニタイズ
        if type(ids) != list:
            ids = [ids]

        # TODO use map to filter
        records = session\
            .query(Hanchans)\
            .filter(Hanchans.id.in_([int(s) for s in ids]))\
            .order_by(Hanchans.id)\
            .all()

        return [
            Hanchan(
                line_room_id=record.room_id,
                raw_scores=json.loads(record.raw_scores),
                converted_scores=json.loads(record.converted_scores),
                match_id=record.match_id,
                status=record.status,
            )
            for record in records
        ]

    def find_all(self, session):
        records = session\
            .query(Hanchans)\
            .order_by(Hanchans.id)\
            .all()

        return [
            Hanchan(
                line_room_id=record.room_id,
                raw_scores=json.loads(record.raw_scores),
                converted_scores=json.loads(record.converted_scores),
                match_id=record.match_id,
                status=record.status,
            )
            for record in records
        ]

    def create(self, session, new_hanchan):
        hanchan = Hanchans(
            room_id=new_hanchan.line_room_id,
            match_id=new_hanchan.match_id,
            raw_scores=json.dumps(new_hanchan.raw_scores),
            converted_scores=json.dumps(new_hanchan.converted_scores),
            status=new_hanchan.status,
        )
        session.add(hanchan)

    def delete_by_ids(self, session, ids):
        # 配列をサニタイズ
        if type(ids) != list:
            ids = [ids]

        session\
            .query(Hanchans)\
            .filter(Hanchans.id.in_(ids))\
            .delete(synchronize_session=False)

    def update_raw_score_of_user_by_room_id(
        self,
        session,
        line_room_id,
        line_user_id,
        raw_score=None,
    ):
        if line_room_id is None:
            raise ValueError

        record = session\
            .query(Hanchans).filter(and_(
                Hanchans.room_id == line_room_id,
                Hanchans.status == 1,
            ))\
            .order_by(desc(Hanchans.id))\
            .first()

        if record is None:
            return None

        raw_scores = json.loads(record.raw_scores)
        if line_user_id is None:
            raw_scores = {}
        elif raw_score is None:
            raw_scores.pop(line_user_id)
        else:
            raw_scores[line_user_id] = raw_score
        record.raw_scores = json.dumps(raw_scores)

        return Hanchan(
            line_room_id=record.room_id,
            raw_scores=json.loads(record.raw_scores),
            converted_scores=json.loads(record.converted_scores),
            match_id=record.match_id,
            status=record.status,
        )

    def update_status_by_line_room_id(
        self,
        session,
        line_room_id,
        status,
    ):
        record = session\
            .query(Hanchans).filter(and_(
                Hanchans.room_id == line_room_id,
                Hanchans.status == 1,
            ))\
            .order_by(desc(Hanchans.id))\
            .first()

        if record is None:
            return None

        record.status = status

        return Hanchan(
            line_room_id=record.room_id,
            raw_scores=json.loads(record.raw_scores),
            converted_scores=json.loads(record.converted_scores),
            match_id=record.match_id,
            status=record.status,
        )

    def update_status_by_id_and_line_room_id(
        self,
        session,
        hanchan_id,
        line_room_id,
        status,
    ):
        record = session\
            .query(Hanchans).filter(and_(
                Hanchans.id == hanchan_id,
                Hanchans.room_id == line_room_id,
                Hanchans.status == 1,
            ))\
            .order_by(desc(Hanchans.id))\
            .first()

        if record is None:
            return None

        record.status = status

        return Hanchan(
            line_room_id=record.room_id,
            raw_scores=json.loads(record.raw_scores),
            converted_scores=json.loads(record.converted_scores),
            match_id=record.match_id,
            status=record.status,
        )

    def update_one_converted_score_by_line_room_id(
        self,
        session,
        line_room_id,
        converted_scores,
    ):
        record = session\
            .query(Hanchans).filter(and_(
                Hanchans.room_id == line_room_id,
                Hanchans.status == 1,
            ))\
            .order_by(desc(Hanchans.id))\
            .first()

        if record is None:
            return None

        record.converted_scores = json.dumps(converted_scores)

        return Hanchan(
            _id=record.id,
            line_room_id=record.room_id,
            raw_scores=json.loads(record.raw_scores),
            converted_scores=json.loads(record.converted_scores),
            match_id=record.match_id,
            status=record.status,
        )
