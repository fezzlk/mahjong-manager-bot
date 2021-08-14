"""
users repository
"""

from models import Users


class UsersRepository:

    def find_by_user_id(session, user_id):
        return session\
            .query(Users)\
            .filter(Users.user_id == user_id)\
            .first()
                    
    def find_by_name(session, name):
        return session\
            .query(Users)\
            .filter(Users.name == name)\
            .first()

    def find_by_ids(session, ids):
        # 配列にサニタイズ
        if type(ids) != list:
            ids = [ids]

        return session\
            .query(Users)\
            .filter(Users.id.in_(ids))\
            .order_by(Users.id)\
            .all()

    def find_all(session):
        return session\
            .query(Users)\
            .order_by(Users.id)\
            .all()

    def create(session, name, user_id, mode):
        new_user = Users(
            name=name,
            user_id=user_id,
            mode=mode,
        )
        session.add(new_user)
        return new_user

    def delete_by_user_id(session, user_id):
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
