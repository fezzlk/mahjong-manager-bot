from typing import List
from db_models import YakumanUserModel
from DomainModel.entities.YakumanUser import YakumanUser
from sqlalchemy.orm.session import Session as BaseSession


class YakumanUserRepository:

    def create(
        self,
        session: BaseSession,
        new_yakuman_user: YakumanUser,
    ) -> YakumanUser:
        record = YakumanUserModel(
            line_user_id=new_yakuman_user.line_user_id,
            hanchan_id=new_yakuman_user.hanchan_id
        )
        session.add(record)
        new_yakuman_user._id = record.id
        return new_yakuman_user

    def find_by_user_ids(
        self,
        session: BaseSession,
        user_ids: List[int],
    ) -> List[YakumanUser]:
        records = session.query(YakumanUserModel).filter(
            YakumanUserModel.user_id.in_([int(s) for s in user_ids])) .all()

        return [
            self._mapping_record_to_domain(record)
            for record in records
        ]

    def find_by_hanchan_ids(
        self,
        session: BaseSession,
        hanchan_ids: List[int],
    ) -> List[YakumanUser]:
        records = session.query(YakumanUserModel).filter(
            YakumanUserModel.hanchan_id.in_([int(s) for s in hanchan_ids])) .all()

        return [
            self._mapping_record_to_domain(record)
            for record in records
        ]

    def _mapping_record_to_domain(
        self,
        record: YakumanUser
    ) -> YakumanUser:
        return YakumanUser(
            _id=record.id,
            hanchan_id=record.hanchan_id,
            line_user_id=record.line_user_id,
        )
