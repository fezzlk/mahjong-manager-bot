from typing import List
from db_models import UserMatchModel
from DomainModel.IRepositories.IUserMatchRepository import IUserMatchRepository
from DomainModel.entities.UserMatch import UserMatch
from sqlalchemy.orm.session import Session as BaseSession


class UserMatchRepository(IUserMatchRepository):

    def create(
        self,
        session: BaseSession,
        new_user_match: UserMatch,
    ) -> UserMatch:
        record = UserMatchModel(
            user_id=new_user_match.user_id,
            match_id=new_user_match.match_id,
        )
        session.add(record)
        session.commit()
        new_user_match._id = record.id
        return new_user_match

    def find_by_user_ids(
        self,
        session: BaseSession,
        user_ids: List[int]
    ) -> List[UserMatch]:
        records = session\
            .query(UserMatchModel)\
            .filter(UserMatchModel.user_id.in_(user_ids))\
            .order_by(UserMatchModel.id)\
            .all()

        return [
            self._mapping_record_to_user_match_domain(record)
            for record in records
        ]

    def _mapping_record_to_user_match_domain(
            self, record: UserMatchModel) -> UserMatch:
        return UserMatch(
            _id=record.id,
            user_id=record.user_id,
            match_id=record.match_id,
        )
