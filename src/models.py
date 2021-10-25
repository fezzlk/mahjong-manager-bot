"""models"""

# from marshmallow import Schema, fields
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
    # user_id is unique
    user_id = Column(String(255), nullable=False)
    zoom_id = Column(String(255), nullable=True)
    mode = Column(String(255), nullable=False)
    # jantama_name is unique
    jantama_name = Column(String(255), nullable=True)
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

    def __init__(self, name, user_id, mode, zoom_id=None, jantama_name=None):
        self.name = name
        self.zoom_id = zoom_id
        self.jantama_name = jantama_name
        self.user_id = user_id
        self.mode = mode

    @staticmethod
    def add_column(engine, column_name):
        column = Column(column_name, String(255), nullable=True)
        column_type = column.type.compile(engine.dialect)
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                       (Users.__tablename__, column_name, column_type))


class Rooms(Base):
    """
    Room model
    """

    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # room_id is unique
    room_id = Column(String(255), nullable=False)
    zoom_url = Column(String(255), nullable=True)
    mode = Column(String(255), nullable=False)
    users = relationship(
        "Users",
        secondary=association_table_user_room,
        back_populates="rooms"
    )

    def __init__(self, room_id, mode, zoom_url):
        self.room_id = room_id
        self.mode = mode
        self.zoom_url = zoom_url

    @staticmethod
    def add_column(engine, column_name):
        column = Column(column_name, String(255), nullable=True)
        column_type = column.type.compile(engine.dialect)
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                       (Rooms.__tablename__, column_name, column_type))


class Hanchans(Base):
    """
    Hanchan model
    """

    __tablename__ = 'hanchans'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    room_id = Column(String(255), nullable=False)
    raw_scores = Column(String(255), nullable=True)
    converted_scores = Column(String(255), nullable=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    # status:
    # 0: disabled
    # 1: active
    # 2: archive
    status = Column(Integer, nullable=False)

    def __init__(
        self,
        room_id,
        match_id,
        status,
        raw_scores={},
        converted_scores={},
    ):
        self.room_id = room_id
        self.raw_scores = json.dumps(raw_scores)
        self.converted_scores = json.dumps(converted_scores)
        self.match_id = match_id
        self.status = status

    @staticmethod
    def add_column(engine, column_name):
        column = Column(column_name, String(255), nullable=True)
        column_type = column.type.compile(engine.dialect)
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                       (Hanchans.__tablename__, column_name, column_type))

#     @staticmethod
#     def clone(engine):
#         engine.execute('SELECT * INTO hanchans FROM results')


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

    def __init__(self, line_room_id, hanchan_ids, status):
        self.room_id = line_room_id
        self.result_ids = json.dumps(hanchan_ids),
        self.status = status

    @staticmethod
    def add_column(engine, column_name):
        column = Column(column_name, String(255), nullable=True)
        column_type = column.type.compile(engine.dialect)
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                       (Matches.__tablename__, column_name, column_type))


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

    @staticmethod
    def add_column(engine, column_name):
        column = Column(column_name, String(255), nullable=True)
        column_name = column.compile(dialect=engine.dialect)
        column_type = column.type.compile(engine.dialect)
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                       (Configs.__tablename__, column_name, column_type))


# class Advise(Base):
#     """
#     Advise model
#     """

#     __tablename__ = 'advises'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     phrase = Column(String(255), nullable=False)
#     match_id = Column(Integer, ForeignKey("matches.id"))

#     def __init__(self, user_id, phrase):
#         self.user_id = user_id
#         self.phrase = phrase
