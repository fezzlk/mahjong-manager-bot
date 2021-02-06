"""models"""

from sqlalchemy import Column, String, Integer, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from db_setting import Base
import json

association_table_user_match = Table(
    'user_match', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('match_id', Integer, ForeignKey('matches.id'))
)

association_table_user_room = Table(
    'user_room', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('room_id', Integer, ForeignKey('rooms.id'))
)


class Users(Base):
    """
    User model
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    user_id = Column(String(255), nullable=False)
    mode = Column(String(255), nullable=False)
    matches = relationship(
        "Matches",
        secondary=association_table_user_match,
        back_populates="users"
    )
    rooms = relationship(
        "Rooms",
        secondary=association_table_user_room,
        back_populates="users"
    )

    def __init__(self, name, user_id, jantama_name, mode):
        self.name = name
        self.jantama_name = jantama_name
        self.user_id = user_id
        self.mode = mode


class Rooms(Base):
    """
    Room model
    """

    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(String(255), nullable=False)
    mode = Column(String(255), nullable=False)
    users = relationship(
        "Users",
        secondary=association_table_user_room,
        back_populates="rooms"
    )

    def __init__(self, room_id, mode):
        self.room_id = room_id
        self.mode = mode


class Results(Base):
    """
    Result model
    """

    __tablename__ = 'results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(String(255), nullable=False)
    points = Column(String(255), nullable=True)
    result = Column(String(255), nullable=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    # status:
    # 0: disabled
    # 1: active
    # 2: archive
    status = Column(Integer, nullable=False)

    def __init__(self, room_id, match_id):
        self.room_id = room_id
        self.points = json.dumps({})
        self.match_id = match_id
        self.status = 1


class Matches(Base):
    """
    Match model
    """

    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(String(255), nullable=False)
    result_ids = Column(String(255))
    # status:
    # 0: disabled
    # 1: active
    # 2: archive
    status = Column(Integer, nullable=False)
    users = relationship(
        "Users",
        secondary=association_table_user_match,
        back_populates="matches"
    )
    created_at = Column(DateTime, nullable=False,
                        server_default=current_timestamp())

    def __init__(self, room_id):
        self.room_id = room_id
        self.result_ids = ','.join([])
        self.status = 1


class Configs(Base):
    """
    Config model
    """

    __tablename__ = 'configs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    target_id = Column(String(255), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)

    def __init__(self, target_id, key, value):
        self.target_id = target_id
        self.key = key
        self.value = value
