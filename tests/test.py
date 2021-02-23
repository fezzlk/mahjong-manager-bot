
import set_local_env  # for local dev env

import os
from flask import Flask
from services import Services
from router import Router
app = Flask(__name__)

services = Services(app)
router = Router(services)


class Event:
    def __init__(self, message_text, message_type='text', event_type='message', source_type='room'):
        self.type = 'message'
        self.source = Source(source_type)
        self.message = Message(message_text, message_type)


class Source:
    def __init__(self, source_type='room'):
        self.type = source_type
        self.user_id = os.environ["TEST_USER_ID"]
        self.room_id = os.environ["TEST_ROOM_ID"]


class Message:
    def __init__(self, text, message_type='text'):
        self.type = message_type
        self.text = text


def change_mode():
    message_event1 = Event('_input')
    router.root(message_event1)
    mode = services.room_service.get_mode()
    assert mode == services.room_service.modes.input
