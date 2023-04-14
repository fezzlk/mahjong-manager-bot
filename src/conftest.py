# flake8: noqa
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()
os.environ.setdefault('IS_TEST', 'True')

from db_setting import Engine, Session
from db_models import Base
import pytest

import server

from ApplicationService import (
    reply_service,
    request_info_service,
)

@pytest.fixture(scope='function', autouse=True)
def reset_db_and_services():
    Base.metadata.drop_all(bind=Engine)
    Base.metadata.create_all(bind=Engine)
    request_info_service.delete_req_info()
    reply_service.reset()
