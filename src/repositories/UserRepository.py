from typing import List
from db_models import UserModel
from domains.IRepositories.IUserRepository import IUserRepository
from domains.entities.User import User, UserMode
from sqlalchemy.orm.session import Session as BaseSession


class UserRepository(IUserRepository):

    def create(
        self,
        session: BaseSession,
        new_user: User,
    ) -> User:
        record = UserModel(
            line_user_name=new_user.line_user_name,
            line_user_id=new_user.line_user_id,
            zoom_url=new_user.zoom_url,
            mode=new_user.mode.value,
            jantama_name=new_user.jantama_name,
        )
        session.add(record)
        session.commit()
        new_user._id = record.id
        return new_user

    def delete_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> int:
        delete_count = session\
            .query(UserModel)\
            .filter(UserModel.id.in_(ids))\
            .delete(synchronize_session=False)

        return delete_count

    def delete_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
    ) -> int:
        delete_count = session\
            .query(UserModel)\
            .filter(UserModel.line_user_id == line_user_id)\
            .delete()

        return delete_count

    def find_all(
        self,
        session: BaseSession,
    ) -> List[User]:
        records = session\
            .query(UserModel)\
            .order_by(UserModel.id)\
            .all()

        return [
            self._mapping_record_to_user_domain(record)
            for record in records
        ]

    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> List[User]:
        records = session\
            .query(UserModel)\
            .filter(UserModel.id.in_(ids))\
            .order_by(UserModel.id)\
            .all()

        return [
            self._mapping_record_to_user_domain(record)
            for record in records
        ]

    def find_one_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
    ) -> User:
        record = session\
            .query(UserModel)\
            .filter(UserModel.line_user_id == line_user_id)\
            .first()

        if record is None:
            return None

        return self._mapping_record_to_user_domain(record)

    def find_one_by_name(
        self,
        session: BaseSession,
        line_user_name: str,
    ) -> User:
        records = session\
            .query(UserModel)\
            .filter(UserModel.line_user_name == line_user_name)\
            .all()

        if len(records) == 0:
            return None

        if len(records) > 1:
            print("warning: find multi users by line_user_name")

        return self._mapping_record_to_user_domain(records[0])

    def update_one_mode_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
        mode: UserMode,
    ) -> User:
        record = session\
            .query(UserModel)\
            .filter(UserModel.line_user_id == line_user_id)\
            .first()

        if record is None:
            return None

        record.mode = mode.value

        return self._mapping_record_to_user_domain(record)

    def update_one_zoom_url_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
        zoom_url: str,
    ) -> User:
        record = session\
            .query(UserModel)\
            .filter(UserModel.line_user_id == line_user_id)\
            .first()

        if record is None:
            return None

        record.zoom_url = zoom_url

        return self._mapping_record_to_user_domain(record)

    def _mapping_record_to_user_domain(self, record: UserModel) -> User:
        return User(
            _id=record.id,
            line_user_name=record.line_user_name,
            line_user_id=record.line_user_id,
            zoom_url=record.zoom_url,
            mode=UserMode[record.mode],
            jantama_name=record.jantama_name,
        )
