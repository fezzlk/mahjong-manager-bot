from typing import List
from db_models import UserGroupModel
from DomainModel.IRepositories.IUserGroupRepository import IUserGroupRepository
from DomainModel.entities.UserGroup import UserGroup
from sqlalchemy.orm.session import Session as BaseSession


class UserGroupRepository(IUserGroupRepository):

    def create(
        self,
        session: BaseSession,
        new_user_group: UserGroup,
    ) -> UserGroup:
        record = UserGroupModel(
            line_user_id=new_user_group.line_user_id,
            line_group_id=new_user_group.line_group_id,
        )
        session.add(record)
        session.commit()
        return new_user_group

    def find_all(
        self,
        session: BaseSession,
    ) -> List[UserGroup]:
        records = session\
            .query(UserGroupModel)\
            .order_by(UserGroupModel.line_group_id, UserGroupModel.line_user_id)\
            .all()

        return [
            self._mapping_record_to_user_group_domain(record)
            for record in records
        ]

    def find_by_line_group_id(
        self,
        session: BaseSession,
        line_group_id: str
    ) -> List[UserGroup]:
        records = session\
            .query(UserGroupModel)\
            .filter(
                UserGroupModel.line_group_id == line_group_id,
            )\
            .all()

        return [
            self._mapping_record_to_user_group_domain(record)
            for record in records
        ]

    def find_one(
        self,
        session: BaseSession,
        line_group_id: str,
        line_user_id: str,
    ) -> UserGroup:
        record = session\
            .query(UserGroupModel)\
            .filter(
                UserGroupModel.line_group_id == line_group_id,
                UserGroupModel.line_user_id == line_user_id,
            )\
            .first()

        if record is None:
            return None

        return self._mapping_record_to_user_group_domain(record)

    def _mapping_record_to_user_group_domain(
            self, record: UserGroupModel) -> UserGroup:
        return UserGroup(
            line_user_id=record.line_user_id,
            line_group_id=record.line_group_id,
        )
