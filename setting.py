from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
uri = os.environ["DATABASE_URL"]
# Engine の作成
Engine = create_engine(name_or_url=uri)

# Session の作成
session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=Engine
)

BaseModel = declarative_base()
