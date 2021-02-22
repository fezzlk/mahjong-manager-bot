
import set_local_env  # for local dev env

import os
from flask import Flask
from services import Services
from router import Router
app = Flask(__name__)

services = Services(app)
router = Router(services)


class Event:
    def __init__(self):
        self.type = 'message'
        self.source = Source()
        self.message = Message()


class Source:
    def __init__(self):
        self.type = 'room'
        self.user_id = os.environ["TEST_USER_ID"]
        self.room_id = os.environ["TEST_ROOM_ID"]


class Message:
    def __init__(self):
        self.type = 'text'
        self.text = 'hoge'


def test_hoge():
    a = 1
    b = 1
    assert a == b


def test_fuga():
    a = 1
    b = 1
    event = Event()
    router.root(event)
    assert a == b
