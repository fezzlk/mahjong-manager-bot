# flake8: noqa
import sys
import os

sys.path.append(os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + "/../"))
sys.path.append("/src")

from dotenv import load_dotenv
load_dotenv()

from db_setting import Base, Engine, Session
import pytest

@pytest.fixture(scope='function', autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=Engine)
    Base.metadata.create_all(bind=Engine)
