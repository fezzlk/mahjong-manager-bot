from models import Users
from domains.User import User, UserMode
from sqlalchemy.orm.session import Session as BaseSession


class UserRepository:

    def find_one_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
    ) -> User:
        record = session\
            .query(Users)\
            .filter(Users.user_id == line_user_id)\
            .first()

        if record is None:
            return None

        return User(
            name=record.name,
            line_user_id=record.user_id,
            zoom_url=record.zoom_id,
            mode=UserMode[record.mode],
            jantama_name=record.jantama_name,
        )

    def find_one_by_name(
        self,
        session: BaseSession,
        name: str,
    ) -> User:
        records = session\
            .query(Users)\
            .filter(Users.name == name)\
            .all()

        if len(records) == 0:
            return None

        if len(records) > 1:
            print("warning: find multi users by name")

        return User(
            name=records[0].name,
            line_user_id=records[0].user_id,
            zoom_url=records[0].zoom_id,
            mode=UserMode[records[0].mode],
            jantama_name=records[0].jantama_name,
        )

    def find_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> list:
        records = session\
            .query(Users)\
            .filter(Users.id.in_(ids))\
            .order_by(Users.id)\
            .all()

        return [
            User(
                name=record.name,
                line_user_id=record.user_id,
                zoom_url=record.zoom_id,
                mode=UserMode[record.mode],
                jantama_name=record.jantama_name,
            )
            for record in records
        ]

    def find_all(
        self,
        session: BaseSession,
    ) -> list:
        records = session\
            .query(Users)\
            .order_by(Users.id)\
            .all()

        return [
            User(
                _id=record.id,
                name=record.name,
                line_user_id=record.user_id,
                zoom_url=record.zoom_id,
                mode=UserMode[record.mode],
                jantama_name=record.jantama_name,
            )
            for record in records
        ]

    def create(
        self,
        session: BaseSession,
        new_user: User,
    ) -> None:
        record = Users(
            name=new_user.name,
            user_id=new_user.line_user_id,
            zoom_id=new_user.zoom_url,
            mode=new_user.mode.value,
            jantama_name=new_user.jantama_name,
        )
        session.add(record)

    def delete_one_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
    ) -> None:
        session\
            .query(Users)\
            .filter(Users.user_id == line_user_id)\
            .delete()

    def delete_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> None:
        session\
            .query(Users)\
            .filter(Users.id.in_(ids))\
            .delete(synchronize_session=False)

    def update_one_mode_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
        mode: UserMode,
    ) -> User:
        record = session\
            .query(Users)\
            .filter(Users.user_id == line_user_id)\
            .first()

        if record is None:
            return None

        record.mode = mode.value

        return User(
            _id=record.id,
            name=record.name,
            line_user_id=record.user_id,
            zoom_url=record.zoom_id,
            mode=UserMode[record.mode],
            jantama_name=record.jantama_name,
        )

    def update_one_zoom_url_by_line_user_id(
        self,
        session: BaseSession,
        line_user_id: str,
        zoom_url: str,
    ) -> User:
        record = session\
            .query(Users)\
            .filter(Users.user_id == line_user_id)\
            .first()

        if record is None:
            return None

        record.zoom_id = zoom_url

        return User(
            _id=record.id,
            name=record.name,
            line_user_id=record.user_id,
            zoom_url=record.zoom_id,
            mode=UserMode[record.mode],
            jantama_name=record.jantama_name,
        )
