"""database settings"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Engine = create_engine(os.environ["DATABASE_URL"])

session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=Engine
)

Base = declarative_base()
