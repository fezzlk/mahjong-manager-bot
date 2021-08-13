"""models"""

# from marshmallow import Schema, fields
from sqlalchemy import Column, String, Integer, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from server import Base, Engine
import json


# class ResultSchema(Schema):
#     room_id = fields.Str()

#     # created_at = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')


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
    zoom_id = Column(String(255), nullable=True)
    mode = Column(String(255), nullable=False)
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

    def __init__(self, name, user_id, mode, jantama_name=''):
        self.name = name
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
    room_id = Column(String(255), nullable=False)
    zoom_url = Column(String(255), nullable=True)
    mode = Column(String(255), nullable=False)
    users = relationship(
        "Users",
        secondary=association_table_user_room,
        back_populates="rooms"
    )

    def __init__(self, room_id, mode):
        self.room_id = room_id
        self.mode = mode

    @staticmethod
    def add_column(engine, column_name):
        column = Column(column_name, String(255), nullable=True)
        column_type = column.type.compile(engine.dialect)
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                       (Rooms.__tablename__, column_name, column_type))


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

    def __init__(self, room_id, match_id, points={}):
        self.room_id = room_id
        self.points = json.dumps(points)
        self.match_id = match_id
        self.status = 1

    @staticmethod
    def add_column(engine, column_name):
        column = Column(column_name, String(255), nullable=True)
        column_type = column.type.compile(engine.dialect)
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                       (Results.__tablename__, column_name, column_type))

    @staticmethod
    def clone(engine):
        engine.execute('SELECT * INTO hanchans FROM results')

    # @staticmethod
    # def get_json(engine):
    #     res = ResultSchema().dump(Results.query.all().data)
    #     print(res)
    #     return res


class Hanchans(Base):
    """
    Hanchan model
    """

    __tablename__ = 'hanchans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(String(255), nullable=False)
    raw_scores = Column(String(255), nullable=True)
    converted_scores = Column(String(255), nullable=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    # status:
    # 0: disabled
    # 1: active
    # 2: archive
    status = Column(Integer, nullable=False)

    # def __init__(self, id, room_id, match_id, raw_scores={}, converted_scores, status):
    #     self.id = id
    #     self.room_id = room_id
    #     self.raw_scores = json.dumps(raw_scores)
    #     self.match_id = match_id
    #     self.status = 1

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

    def __init__(self, room_id):
        self.room_id = room_id
        self.result_ids = json.dumps([])
        self.status = 1

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
