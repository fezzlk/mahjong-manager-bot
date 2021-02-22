
import set_local_env  # for local dev env

import os
from flask import Flask
from services import Services
from router import Router
app = Flask(__name__)

services = Services(app)
router = Router(services)


def test_hoge():
    a = 1
    b = 1
    assert a == b


def test_fuga():
    a = 1
    b = 1
    event = {
        'type': 'message',
        'source': {
            'type': 'room',
            'user_id': os.environ["TEST_USER_ID"],
            'room_id': os.environ["TEST_ROOM_ID"],
        },
        'message': {
            'type': 'text',
            'text': 'hoge',
        },
    }
    router.root(event)
    assert a == b
