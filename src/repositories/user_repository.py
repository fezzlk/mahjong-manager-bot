"""
users repository
"""

from models import Users
from domains.user import User, UserMode


class UserRepository:

    def find_one_by_line_user_id(session, user_id):
        if user_id is None:
            raise ValueError

        record = session\
            .query(Users)\
            .filter(Users.user_id == user_id)\
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

    def find_one_by_name(session, name):
        if name is None:
            raise ValueError

        records = session\
            .query(Users)\
            .filter(Users.name == name)\
            .all()

        if len(records) == 0:
            return None

        if len(records) > 1:
            # logger を使う
            print("warning: find multi users by name")

        return User(
            name=records[0].name,
            line_user_id=records[0].user_id,
            zoom_url=records[0].zoom_id,
            mode=UserMode[records[0].mode],
            jantama_name=records[0].jantama_name,
        )

    def find_by_ids(session, ids):
        # 配列にサニタイズ
        if type(ids) != list:
            ids = [ids]

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

    def find_all(session):
        records = session\
            .query(Users)\
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

    def create(session, new_user):
        record = Users(
            name=new_user.name,
            user_id=new_user.line_user_id,
            zoom_id=new_user.zoom_url,
            mode=new_user.mode.value,
            jantama_name=new_user.jantama_name,
        )
        session.add(record)

    def delete_one_by_line_user_id(session, user_id):
        if user_id is None:
            raise ValueError

        session\
            .query(Users)\
            .filter(Users.user_id == user_id)\
            .delete()

    def delete_by_ids(session, ids):
        # 配列にサニタイズ
        if type(ids) != list:
            ids = [ids]

        session\
            .query(Users)\
            .filter(Users.id.in_(ids))\
            .delete(synchronize_session=False)
