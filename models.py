"""models"""

from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from db_setting import Base

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

    def __init__(self, name, user_id, mode):
        self.name = name
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

    def __init__(self, name, user_id, mode):
        self.name = name
        self.user_id = user_id
        self.mode = mode


class Results(Base):
    """
    Result model
    """

    __tablename__ = 'results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(String(255), nullable=False)
    points = Column(String(255), nullable=True)
    match_id = Column(Integer, ForeignKey("matches.id"))

    def __init__(self, room_id, match_id):
        self.room_id = room_id
        self.points = "{}"
        self.match_id = match_id


class Matches(Base):
    """
    Match model
    """

    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, autoincrement=True)
    users = relationship(
        "Users",
        secondary=association_table_user_match,
        back_populates="matches"
    )
    results = relationship("Results")


class Configs(Base):
    """
    Config model
    """

    __tablename__ = 'configs'

    key = Column(String(255), nullable=False, primary_key=True)
    value = Column(String(255), nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value
