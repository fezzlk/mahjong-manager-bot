from models import Hanchans
from sqlalchemy import and_, desc
from domains.Hanchan import Hanchan
from sqlalchemy.orm.session import Session as BaseSession
import json


class HanchanRepository:

    def create(
        self,
        session: BaseSession,
        new_hanchan: Hanchan,
    ) -> None:
        hanchan = Hanchans(
            room_id=new_hanchan.line_room_id,
            match_id=new_hanchan.match_id,
            raw_scores=json.dumps(new_hanchan.raw_scores),
            converted_scores=json.dumps(new_hanchan.converted_scores),
            status=new_hanchan.status,
        )
        session.add(hanchan)

    def delete_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> None:
        session\
            .query(Hanchans)\
            .filter(Hanchans.id.in_(ids))\
            .delete(synchronize_session=False)

    def find_all(
        self,
        session: BaseSession,
    ) -> list:
        records = session\
            .query(Hanchans)\
            .order_by(Hanchans.id)\
            .all()

        return [
            Hanchan(
                _id=record.id,
                line_room_id=record.room_id,
                raw_scores=(json.loads(record.raw_scores) if record.raw_scores is not None else {}),
                converted_scores=(json.loads(record.converted_scores) if record.converted_scores is not None else {}),
                match_id=record.match_id,
                status=record.status,
            )
            for record in records
        ]

    def find_one_by_id_and_line_room_id(
        self,
        session: BaseSession,
        target_id: str,
        line_room_id: str,
    ) -> Hanchan:
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
            _id=record.id,
            line_room_id=record.room_id,
            raw_scores=(json.loads(record.raw_scores) if record.raw_scores is not None else {}),
            converted_scores=(json.loads(record.converted_scores) if record.converted_scores is not None else {}),
            match_id=record.match_id,
            status=record.status,
        )

    def find_one_by_line_room_id_and_status(
        self,
        session: BaseSession,
        line_room_id: str,
        status: int,
    ) -> Hanchan:
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
            _id=record.id,
            line_room_id=record.room_id,
            raw_scores=(json.loads(record.raw_scores) if record.raw_scores is not None else {}),
            converted_scores=(json.loads(record.converted_scores) if record.converted_scores is not None else {}),
            match_id=record.match_id,
            status=record.status,
        )

    def find_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> list:
        # TODO use map to filter
        records = session\
            .query(Hanchans)\
            .filter(Hanchans.id.in_([int(s) for s in ids]))\
            .order_by(Hanchans.id)\
            .all()

        return [
            Hanchan(
                _id=record.id,
                line_room_id=record.room_id,
                raw_scores=(json.loads(record.raw_scores) if record.raw_scores is not None else {}),
                converted_scores=(json.loads(record.converted_scores) if record.converted_scores is not None else {}),
                match_id=record.match_id,
                status=record.status,
            )
            for record in records
        ]

    def update_one_converted_score_by_line_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        converted_scores: dict,
    ) -> Hanchan:
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
            raw_scores=(json.loads(record.raw_scores) if record.raw_scores is not None else {}),
            converted_scores=(json.loads(record.converted_scores) if record.converted_scores is not None else {}),
            match_id=record.match_id,
            status=record.status,
        )

    def update_raw_score_of_user_by_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        line_user_id: str,
        raw_score: int = None,
    ) -> Hanchan:
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
            _id=record.id,
            line_room_id=record.room_id,
            raw_scores=(json.loads(record.raw_scores) if record.raw_scores is not None else {}),
            converted_scores=(json.loads(record.converted_scores) if record.converted_scores is not None else {}),
            match_id=record.match_id,
            status=record.status,
        )

    def update_status_by_id_and_line_room_id(
        self,
        session: BaseSession,
        hanchan_id: int,
        line_room_id: str,
        status: int,
    ) -> Hanchan:
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
            _id=record.id,
            line_room_id=record.room_id,
            raw_scores=(json.loads(record.raw_scores) if record.raw_scores is not None else {}),
            converted_scores=(json.loads(record.converted_scores) if record.converted_scores is not None else {}),
            match_id=record.match_id,
            status=record.status,
        )

    def update_status_by_line_room_id(
        self,
        session: BaseSession,
        line_room_id: str,
        status: int,
    ) -> Hanchan:
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
            _id=record.id,
            line_room_id=record.room_id,
            raw_scores=(json.loads(record.raw_scores) if record.raw_scores is not None else {}),
            converted_scores=(json.loads(record.converted_scores) if record.converted_scores is not None else {}),
            match_id=record.match_id,
            status=record.status,
        )
