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

association_table_user_group = Table(
    'user_group', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)


class UserSchema(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_user_name = Column(String(255), nullable=False)
    line_user_id = Column(String(255), nullable=False)
    zoom_url = Column(String(255), nullable=True)
    mode = Column(String(255), nullable=False)
    jantama_name = Column(String(255), nullable=True)
    matches = relationship(
        "Matches",
        secondary=association_table_user_match,
        back_populates="users"
    )
    groups = relationship(
        "Groups",
        secondary=association_table_user_group,
        back_populates="users"
    )

    def __init__(
        self,
        line_user_name,
        line_user_id,
        mode,
        zoom_url=None,
        jantama_name=None
    ):
        self.line_user_name = line_user_name
        self.zoom_url = zoom_url
        self.jantama_name = jantama_name
        self.line_user_id = line_user_id
        self.mode = mode

    @staticmethod
    def add_column(engine, column_name):
        column = Column(column_name, String(255), nullable=True)
        column_type = column.type.compile(engine.dialect)
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                       (UserSchema.__tablename__, column_name, column_type))


class GroupSchema(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    line_group_id = Column(String(255), nullable=False, unique=True)
    zoom_url = Column(String(255), nullable=True)
    mode = Column(String(255), nullable=False)
    users = relationship(
        "Users",
        secondary=association_table_user_group,
        back_populates="groups"
    )

    def __init__(
        self,
        line_group_id,
        mode,
        zoom_url,
        id=None,
    ):
        if id is not None:
            self.id = id
        self.line_group_id = line_group_id
        self.mode = mode
        self.zoom_url = zoom_url

    @staticmethod
    def add_column(engine, column_name):
        column = Column(column_name, String(255), nullable=True)
        column_type = column.type.compile(engine.dialect)
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                       (GroupSchema.__tablename__, column_name, column_type))


class HanchanSchema(Base):
    __tablename__ = 'hanchans'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    line_group_id = Column(String(255), nullable=False)
    raw_scores = Column(String(255), nullable=True)
    converted_scores = Column(String(255), nullable=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    status = Column(Integer, nullable=False)

    def __init__(
        self,
        line_group_id,
        match_id,
        status,
        raw_scores={},
        converted_scores={},
    ):
        self.line_group_id = line_group_id
        self.raw_scores = json.dumps(raw_scores)
        self.converted_scores = json.dumps(converted_scores)
        self.match_id = match_id
        self.status = status

    @staticmethod
    def add_column(engine, column_name):
        column = Column(column_name, String(255), nullable=True)
        column_type = column.type.compile(engine.dialect)
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                       (HanchanSchema.__tablename__, column_name, column_type))


class MatcheSchema(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_group_id = Column(String(255), nullable=False)
    hanchan_ids = Column(String(255))
    status = Column(Integer, nullable=False)
    users = relationship(
        "Users",
        secondary=association_table_user_match,
        back_populates="matches"
    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=current_timestamp()
    )

    def __init__(self, line_group_id, hanchan_ids, status):
        self.line_group_id = line_group_id
        self.hanchan_ids = json.dumps(hanchan_ids),
        self.status = status

    @staticmethod
    def add_column(engine, column_name):
        column = Column(column_name, String(255), nullable=True)
        column_type = column.type.compile(engine.dialect)
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                       (MatcheSchema.__tablename__, column_name, column_type))


class ConfigSchema(Base):
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
                       (ConfigSchema.__tablename__, column_name, column_type))
