
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
        if source_type == 'room':
            self.room_id = os.environ["TEST_ROOM_ID"]


class Message:
    def __init__(self, text, message_type='text'):
        self.type = message_type
        self.text = text


def set_req_info():
    event1 = Event('hoge')
    router.root(event1)

    # errors = []
    # # replace assertions by conditions
    # if not services.app_service.req_user_id == event1.source.user_id:
    #     errors.append("failed to set req_user_id")
    # if not services.app_service.req_room_id == event1.source.room_id:
    #     errors.append("failed to set req_room_id")
    # # # assert no error message has been registered, else print messages
    # assert not errors, "errors occured:\n{}".format("\n".join(errors))


def change_mode():
    message_event1 = Event('_input')
    router.root(message_event1)


set_req_info()
change_mode()
