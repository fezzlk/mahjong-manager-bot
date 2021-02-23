
import set_local_env  # for local dev env

import os
from flask import Flask
from services import Services
from router import Router
app = Flask(__name__)

services = Services(app)
router = Router(services)


class Event:
    def __init__(self, data, message_type='text', event_type='message', source_type='room'):
        self.type = event_type
        self.source = Source(source_type)
        if self.type == 'message':
            self.message = Message(data, message_type)
        if self.type == 'postback':
            self.postback == Postback(data)


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


class Postback:
    def __init__(self, data=''):
        self.data = data


def test_recieve_message():
    router.root(Event('hoge'))


def test_input():
    errors = []

    router.root(Event('_input'))
    router.root(Event('@a 10000'))
    result = services.results_service.get_current(os.environ["TEST_ROOM_ID"])
    if not result.points == '{"a": 10000}':
        errors.append("failed to input point")
    router.root(Event('@b 20000'))
    router.root(Event('@c 60000'))
    router.root(Event('@f 60000'))
    router.root(Event('@f'))
    router.root(Event('@c 30000'))
    router.root(Event('@d 40000'))

    # assert no error message has been registered, else print messages
    assert not errors, "errors occured:\n{}".format("\n".join(errors))


# def test_input_with_tobi():
#     errors = []

#     router.root(Event('_input'))
#     router.root(Event('@a -10000'))
#     result = services.results_service.get_current(os.environ["TEST_ROOM_ID"])
#     if not result.points == '{"a": -10000}':
#         errors.append("failed to input point")
#     router.root(Event('@b 20000'))
#     router.root(Event('@c 30000'))
#     router.root(Event('@d 60000'))

    # router.root(Event(='_tobi a', event_type='postback))

    # router.root(Event('_input'))
    # router.root(Event('@a -1000'))
    # result = services.results_service.get_current(os.environ["TEST_ROOM_ID"])
    # if not result.points == '{"a": 10000}':
    #     errors.append("failed to input point")
    # router.root(Event('@b -200'))
    # router.root(Event('@c 51200'))
    # router.root(Event('@d 50000'))

    # router.root(Event(='_tobi', event_type='postback))

    # # assert no error message has been registered, else print messages
    # assert not errors, "errors occured:\n{}".format("\n".join(errors))
