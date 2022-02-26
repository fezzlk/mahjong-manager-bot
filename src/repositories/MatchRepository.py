from typing import List
from db_models import MatchModel
from sqlalchemy import and_
from DomainModel.IRepositories.IMatchRepository import IMatchRepository
from DomainModel.entities.Match import Match
from sqlalchemy.orm.session import Session as BaseSession
import json


class MatchRepository(IMatchRepository):

    def create(
        self,
        session: BaseSession,
        new_match: Match,
    ) -> Match:
        record = MatchModel(
            line_group_id=new_match.line_group_id,
            hanchan_ids=new_match.hanchan_ids,
            status=new_match.status,
        )

        session.add(record)
        session.commit()
        new_match._id = record.id
        return new_match

    def find_all(
        self,
        session: BaseSession,
    ) -> List[Match]:
        records = session\
            .query(MatchModel)\
            .order_by(MatchModel.id)\
            .all()

        return [
            self._mapping_record_to_match_domain(record)
            for record in records
        ]

    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[Match],
    ) -> List[Match]:
        records = session\
            .query(MatchModel)\
            .filter(MatchModel.id.in_([int(s) for s in ids]))\
            .order_by(MatchModel.id)\
            .all()

        return [
            self._mapping_record_to_match_domain(record)
            for record in records
        ]

    def find_many_by_line_group_id_and_status(
        self,
        session: BaseSession,
        line_group_id: str,
        status: int,
    ) -> List[Match]:
        records = session\
            .query(MatchModel).filter(and_(
                MatchModel.line_group_id == line_group_id,
                MatchModel.status == status,
            )).order_by(MatchModel.id.desc())\
            .all()

        return [
            self._mapping_record_to_match_domain(record)
            for record in records
        ]

    def find_one_by_line_group_id_and_status(
        self,
        session: BaseSession,
        line_group_id: str,
        status: int,
    ) -> Match:
        record = session\
            .query(MatchModel).filter(and_(
                MatchModel.line_group_id == line_group_id,
                MatchModel.status == status,
            )).order_by(MatchModel.id.desc())\
            .first()

        if record is None:
            return None

        return self._mapping_record_to_match_domain(record)

    def update_one_hanchan_ids_by_id(
        self,
        session: BaseSession,
        match_id: int,
        hanchan_ids: List[int],
    ) -> Match:
        record = session\
            .query(MatchModel).filter(MatchModel.id == match_id)\
            .first()

        if record is None:
            return None

        record.hanchan_ids = json.dumps(hanchan_ids)

        return self._mapping_record_to_match_domain(record)

    def update_one_status_by_id(
        self,
        session: BaseSession,
        match_id: int,
        status: int,
    ) -> Match:
        record = session\
            .query(MatchModel).filter(MatchModel.id == match_id)\
            .first()

        if record is None:
            return None

        record.status = status

        return self._mapping_record_to_match_domain(record)

    def delete_by_ids(
        self,
        session: BaseSession,
        ids: List[int],
    ) -> int:
        delete_count = session\
            .query(MatchModel)\
            .filter(MatchModel.id.in_(ids))\
            .delete(synchronize_session=False)

        return delete_count

    def _mapping_record_to_match_domain(self, record: MatchModel) -> Match:
        return Match(
            _id=record.id,
            line_group_id=record.line_group_id,
            hanchan_ids=json.loads(record.hanchan_ids),
            users=record.users,
            status=record.status,
            created_at=record.created_at,
        )
