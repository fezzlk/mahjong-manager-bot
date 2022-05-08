from typing import List, Optional
from db_models import UserModel
from DomainModel.IRepositories.IUserRepository import IUserRepository
from DomainModel.entities.User import User, UserMode
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
        ids: List[int],
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
            self._mapping_record_to_domain(record)
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
            self._mapping_record_to_domain(record)
            for record in records
        ]

    def find_one_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
    ) -> Optional[User]:
        record = session\
            .query(UserModel)\
            .filter(UserModel.line_user_id == line_user_id)\
            .order_by(UserModel.id)\
            .first()

        if record is None:
            return None

        return self._mapping_record_to_domain(record)

    def find_by_name(
        self,
        session: BaseSession,
        line_user_name: str,
    ) -> List[User]:
        records = session\
            .query(UserModel)\
            .filter(UserModel.line_user_name == line_user_name)\
            .order_by(UserModel.id)\
            .all()
        return [
            self._mapping_record_to_domain(record)
            for record in records
        ]

    def update_one_mode_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
        mode: UserMode,
    ) -> User:
        record = session\
            .query(UserModel)\
            .filter(UserModel.line_user_id == line_user_id)\
            .order_by(UserModel.id)\
            .first()

        if record is None:
            return None

        record.mode = mode.value

        return self._mapping_record_to_domain(record)

    def update_one_zoom_url_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
        zoom_url: str,
    ) -> User:
        record = session\
            .query(UserModel)\
            .filter(UserModel.line_user_id == line_user_id)\
            .order_by(UserModel.id)\
            .first()

        if record is None:
            return None

        record.zoom_url = zoom_url

        return self._mapping_record_to_domain(record)

    def update(
        self,
        session: BaseSession,
        target: User,
    ) -> int:
        updated = UserModel(
            line_user_name=target.line_user_name,
            line_user_id=target.line_user_id,
            zoom_url=target.zoom_url,
            mode=target.mode.value,
            jantama_name=target.jantama_name,
        ).__dict__
        updated.pop('_sa_instance_state')

        result: int = session\
            .query(UserModel)\
            .filter(UserModel.id == target._id)\
            .update(updated)

        return result

    def _mapping_record_to_domain(self, record: UserModel) -> User:
        return User(
            _id=record.id,
            line_user_name=record.line_user_name,
            line_user_id=record.line_user_id,
            zoom_url=record.zoom_url,
            mode=UserMode[record.mode],
            jantama_name=record.jantama_name,
        )
