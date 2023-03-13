from typing import List, Optional
from db_models import WebUserModel
from DomainModel.IRepositories.IWebUserRepository import IWebUserRepository
from DomainModel.entities.WebUser import WebUser
from sqlalchemy.orm.session import Session as BaseSession


class WebUserRepository(IWebUserRepository):

    def create(
        self,
        session: BaseSession,
        new_webuser: WebUser,
    ) -> WebUser:
        record = WebUserModel(
            user_code=new_webuser.user_code,
            name=new_webuser.name,
            email=new_webuser.email,
            linked_line_user_id=new_webuser.linked_line_user_id,
            is_approved_line_user=new_webuser.is_approved_line_user,
        )
        session.add(record)
        session.commit()
        return self._mapping_record_to_webuser_domain(record)

    def find_all(
        self,
        session: BaseSession,
    ) -> List[WebUser]:
        records = session\
            .query(WebUserModel)\
            .order_by(WebUserModel.id)\
            .all()

        return [
            self._mapping_record_to_webuser_domain(record)
            for record in records
        ]

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
            self._mapping_record_to_webuser_domain(record)
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
        
        return self._mapping_record_to_webuser_domain(record)
        
    def update(
        self,
        session: BaseSession,
        target: WebUser,
    ) -> int:
        updated = WebUserModel(
            user_code=target.user_code,
            name=target.name,
            email=target.email,
            linked_line_user_id=target.linked_line_user_id,
            is_approved_line_user=target.is_approved_line_user,
        ).__dict__
        updated.pop('_sa_instance_state')

        result: int = session\
            .query(WebUserModel)\
            .filter(WebUserModel.id == target._id)\
            .update(updated)

        return result

    def _mapping_record_to_webuser_domain(self, record: WebUserModel) -> WebUser:
        return WebUser(
            _id=record.id,
            name=record.name,
            email=record.email,
            linked_line_user_id=record.linked_line_user_id,
            is_approved_line_user=record.is_approved_line_user,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )
