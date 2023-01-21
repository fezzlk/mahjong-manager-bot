"""models"""

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp
from db_setting import Base
import json


class UserGroupModel(Base):
    __tablename__ = 'user_group'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)


class UserMatchModel(Base):
    __tablename__ = 'user_match'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'), primary_key=True)


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_user_name = Column(String(255), nullable=False)
    line_user_id = Column(String(255), nullable=False)
    zoom_url = Column(String(255), nullable=True)
    mode = Column(String(255), nullable=False)
    jantama_name = Column(String(255), nullable=True)
    matches = relationship(
        "MatchModel",
        secondary=UserMatchModel.__tablename__,
        back_populates="users"
    )
    groups = relationship(
        "GroupModel",
        secondary=UserGroupModel.__tablename__,
        back_populates="users"
    )

    def __init__(
        self,
        line_user_name,
        line_user_id,
        mode,
        zoom_url=None,
        jantama_name=None,
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
                       (UserModel.__tablename__, column_name, column_type))


class GroupModel(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    line_group_id = Column(String(255), nullable=False, unique=True)
    zoom_url = Column(String(255), nullable=True)
    mode = Column(String(255), nullable=False)
    users = relationship(
        "UserModel",
        secondary=UserGroupModel.__tablename__,
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
                       (GroupModel.__tablename__, column_name, column_type))


class HanchanModel(Base):
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
                       (HanchanModel.__tablename__, column_name, column_type))


class MatchModel(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_group_id = Column(String(255), nullable=False)
    hanchan_ids = Column(String(255))
    status = Column(Integer, nullable=False)
    users = relationship(
        "UserModel",
        secondary=UserMatchModel.__tablename__,
        back_populates="matches"
    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=current_timestamp()
    )
    chip_scores = Column(String(255), nullable=True)

    def __init__(self, line_group_id, hanchan_ids, status):
        self.line_group_id = line_group_id
        self.hanchan_ids = json.dumps(hanchan_ids),
        self.status = status

    @staticmethod
    def add_column(engine, column_name):
        column = Column(column_name, String(255), nullable=True)
        column_type = column.type.compile(engine.dialect)
        engine.execute('ALTER TABLE %s ADD COLUMN %s %s' %
                       (MatchModel.__tablename__, column_name, column_type))


class ConfigModel(Base):
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
                       (ConfigModel.__tablename__, column_name, column_type))
