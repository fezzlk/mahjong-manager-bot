from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
import env_var

Engine = create_engine(env_var.DATABASE_URL)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=Engine
)

Base: DeclarativeMeta = declarative_base()
