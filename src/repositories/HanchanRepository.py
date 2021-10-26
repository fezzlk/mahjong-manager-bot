from typing import Dict, List
from models import HanchanSchema
from sqlalchemy import and_, desc
from domains.Hanchan import Hanchan
from sqlalchemy.orm.session import Session as BaseSession
import json


class HanchanRepository:

    def create(
        self,
        session: BaseSession,
        new_hanchan: Hanchan,
    ) -> Hanchan:
        record = HanchanSchema(
            line_group_id=new_hanchan.line_group_id,
            match_id=new_hanchan.match_id,
            raw_scores=new_hanchan.raw_scores,
            converted_scores=new_hanchan.converted_scores,
            status=new_hanchan.status,
        )
        session.add(record)
        session.commit()
        new_hanchan._id = record.id
        return new_hanchan

    def delete_by_ids(
        self,
        session: BaseSession,
        ids: List[Hanchan],
    ) -> int:
        delete_count = session\
            .query(HanchanSchema)\
            .filter(HanchanSchema.id.in_(ids))\
            .delete(synchronize_session=False)

        return delete_count

    def find_all(
        self,
        session: BaseSession,
    ) -> List[Hanchan]:
        records = session\
            .query(HanchanSchema)\
            .order_by(HanchanSchema.id)\
            .all()

        return [
            self._mapping_record_to_hanchan_domain(record)
            for record in records
        ]

    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[Hanchan],
    ) -> List[Hanchan]:
        # TODO use map to filter
        records = session\
            .query(HanchanSchema)\
            .filter(HanchanSchema.id.in_([int(s) for s in ids]))\
            .order_by(HanchanSchema.id)\
            .all()

        return [
            self._mapping_record_to_hanchan_domain(record)
            for record in records
        ]

    def find_one_by_id_and_line_group_id(
        self,
        session: BaseSession,
        target_id: str,
        line_group_id: str,
    ) -> Hanchan:
        record = session\
            .query(HanchanSchema)\
            .filter(and_(
                HanchanSchema.line_group_id == line_group_id,
                HanchanSchema.id == target_id,
            ))\
            .first()

        if record is None:
            return None

        return self._mapping_record_to_hanchan_domain(record)

    def find_one_by_line_group_id_and_status(
        self,
        session: BaseSession,
        line_group_id: str,
        status: int,
    ) -> Hanchan:
        record = session\
            .query(HanchanSchema).filter(and_(
                HanchanSchema.line_group_id == line_group_id,
                HanchanSchema.status == status,
            ))\
            .order_by(desc(HanchanSchema.id))\
            .first()

        if record is None:
            return None

        return self._mapping_record_to_hanchan_domain(record)

    def update_one_converted_scores_by_id(
        self,
        session: BaseSession,
        hanchan_id: int,
        converted_scores: Dict[str, int],
    ) -> Hanchan:
        record = session\
            .query(HanchanSchema).filter(HanchanSchema._id == hanchan_id)\
            .first()

        if record is None:
            return None

        record.converted_scores = json.dumps(converted_scores)

        return self._mapping_record_to_hanchan_domain(record)

    def update_one_raw_scores_by_id(
        self,
        session: BaseSession,
        hanchan_id: int,
        raw_scores: Dict[str, int],
    ) -> Hanchan:
        record = session\
            .query(HanchanSchema).filter(HanchanSchema._id == hanchan_id)\
            .first()

        if record is None:
            return None

        record.raw_scores = json.dumps(raw_scores)

        return self._mapping_record_to_hanchan_domain

    def update_status_by_id(
        self,
        session: BaseSession,
        hanchan_id: int,
        status: int,
    ) -> Hanchan:
        record = session\
            .query(HanchanSchema).filter(HanchanSchema.id == hanchan_id)\
            .first()

        if record is None:
            return None

        record.status = status

        return self._mapping_record_to_hanchan_domain(record)

    def _mapping_record_to_hanchan_domain(
        self,
        record: HanchanSchema
    ) -> Hanchan:
        return Hanchan(
            _id=record.id,
            line_group_id=record.line_group_id,
            raw_scores=(
                json.loads(
                    record.raw_scores
                ) if record.raw_scores is not None else {}
            ),
            converted_scores=(
                json.loads(
                    record.converted_scores
                ) if record.converted_scores is not None else {}
            ),
            match_id=record.match_id,
            status=record.status,
        )
