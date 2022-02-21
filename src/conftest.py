# flake8: noqa
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from db_setting import Engine, Session
from db_models import Base
import pytest

import server

@pytest.fixture(scope='function', autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=Engine)
    Base.metadata.create_all(bind=Engine)
