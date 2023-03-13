from contextlib import contextmanager
from db_setting import Session
from sqlalchemy.orm.session import Session as BaseSession

from .ConfigRepository import ConfigRepository
from .UserRepository import UserRepository
from .WebUserRepository import WebUserRepository
from .HanchanRepository import HanchanRepository
from .MatchRepository import MatchRepository
from .UserMatchRepository import UserMatchRepository
from .GroupRepository import GroupRepository

config_repository = ConfigRepository()
user_repository = UserRepository()
web_user_repository = WebUserRepository()
hanchan_repository = HanchanRepository()
match_repository = MatchRepository()
user_match_repository = UserMatchRepository()
group_repository = GroupRepository()


@contextmanager
def session_scope():
    session: BaseSession = Session()

    try:
        yield session  # with as での呼び出し元に session を渡す
        session.commit()  # 呼び出し元の処理が正常に終われば commit
    except Exception:
        session.rollback()  # error が起きた場合 rollback
        raise
    finally:
        session.close()
