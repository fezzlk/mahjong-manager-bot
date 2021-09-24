from contextlib import contextmanager
from db_setting import Session

from .ConfigRepository import ConfigRepository
from .UserRepository import UserRepository
from .HanchanRepository import HanchanRepository
from .MatchRepository import MatchRepository

config_repository = ConfigRepository()
user_repository = UserRepository()
hanchan_repository = HanchanRepository()
match_repository = MatchRepository()


@contextmanager
def session_scope():
    session = Session()

    try:
        yield session  # with as での呼び出し元に session を渡す
        session.commit()  # 呼び出し元の処理が正常に終われば commit
    except Exception:
        session.rollback()  # error が起きた場合 rollback
        raise
    finally:
        session.close()
