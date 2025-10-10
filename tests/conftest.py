# flake8: noqa
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from mongo_client import mongo_client

from dotenv import load_dotenv
load_dotenv()
import env_var
import pytest

import server

from ApplicationService import (
    reply_service,
    request_info_service,
)

@pytest.fixture(scope='function', autouse=True)
def reset_services():
    mongo_client.drop_database(env_var.DATABASE_NAME)
    request_info_service.delete_req_info()
    reply_service.reset()
