from typing import List, Optional
from db_models import WebUserModel
from DomainModel.IRepositories.IWebUserRepository import IWebUserRepository
from DomainModel.entities.WebUser import WebUser
from sqlalchemy.orm.session import Session as BaseSession


class WebUserRepository(IWebUserRepository):

    def create(
        self,
        session: BaseSession,
        new_web_user: WebUser,
    ) -> WebUser:
        record = WebUserModel(
            user_code=new_web_user.user_code,
            name=new_web_user.name,
            email=new_web_user.email,
            linked_line_user_id=new_web_user.linked_line_user_id,
            is_approved_line_user=new_web_user.is_approved_line_user,
        )
        session.add(record)
        session.commit()
        return self._mapping_record_to_web_user_domain(record)

    def find_all(
        self,
        session: BaseSession,
    ) -> List[WebUser]:
        records = session\
            .query(WebUserModel)\
            .order_by(WebUserModel.id)\
            .all()

        return [
            self._mapping_record_to_web_user_domain(record)
            for record in records
        ]

    def find_by_id(
        self,
        session: BaseSession,
        id: str,
    ) -> WebUser:
        record = session\
            .query(WebUserModel)\
            .filter(WebUserModel.id == id)\
            .first()
        
        if record is None:
            return None

        return self._mapping_record_to_web_user_domain(record)

    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> List[WebUser]:
        records = session\
            .query(WebUserModel)\
            .filter(WebUserModel.id.in_(ids))\
            .order_by(WebUserModel.id)\
            .all()
        
        return [
            self._mapping_record_to_web_user_domain(record)
            for record in records
        ]

    def find_one_by_email(
        self,
        session: BaseSession,
        email: str,
    ) -> Optional[WebUser]:
        record = session\
            .query(WebUserModel)\
            .filter(WebUserModel.email == email)\
            .order_by(WebUserModel.id)\
            .first()

        if record is None:
            return None

        return self._mapping_record_to_web_user_domain(record)

    def approve_line(
        self,
        session: BaseSession,
        id: str,
    ) -> Optional[WebUser]:
        record: WebUserModel = session\
            .query(WebUserModel)\
            .filter(WebUserModel.id == id)\
            .first()

        if record is None:
            return None

        record.is_approved_line_user = True
        session.commit()

        return self._mapping_record_to_web_user_domain(record)

    def reset_line(
        self,
        session: BaseSession,
        id: str,
    ) -> Optional[WebUser]:
        record: WebUserModel = session\
            .query(WebUserModel)\
            .filter(WebUserModel.id == id)\
            .first()

        if record is None:
            return None

        record.is_approved_line_user = False
        record.linked_line_user_id = ''
        session.commit()
        return self._mapping_record_to_web_user_domain(record)

    def update_linked_line_user_id(
        self,
        session: BaseSession,
        id: str,
        line_user_id: str,
    ) -> Optional[WebUser]:
        record: WebUserModel = session\
            .query(WebUserModel)\
            .filter(WebUserModel.id == id)\
            .first()

        if record is None:
            return None

        record.linked_line_user_id = line_user_id
        session.commit()
        return self._mapping_record_to_web_user_domain(record)

    def _mapping_record_to_web_user_domain(
        self,
        record: WebUserModel
    ) -> WebUser:
        return WebUser(
            _id=record.id,
            name=record.name,
            email=record.email,
            linked_line_user_id=record.linked_line_user_id,
            is_approved_line_user=record.is_approved_line_user,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )
