
import set_local_env  # for local dev env

import os
import json
from flask import Flask
from services import Services
from router import Router
app = Flask(__name__)

services = Services(app)
router = Router(services)


class Event:
    def __init__(self, data, req_user='a', message_type='text', event_type='message', source_type='room'):
        self.type = event_type
        self.source = Source(req_user, source_type)
        if self.type == 'message':
            self.message = Message(data, message_type)
        if self.type == 'postback':
            self.postback == Postback(data)


class Source:
    def __init__(self, req_user='a', source_type='room'):
        test_user_ids = json.loads(os.environ["TEST_USER_IDS"])
        print(type(test_user_ids))
        print(test_user_ids)
        self.type = source_type
        self.user_id = test_user_ids[req_user]
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


# def test_input():
#     errors = []
#     router.root(Event(req_user='a', event_type='follow'))
#     router.root(Event(req_user='b', event_type='follow'))
#     router.root(Event(req_user='c', event_type='follow'))
#     router.root(Event(req_user='d', event_type='follow'))
#     router.root(Event(req_user='e', event_type='follow'))

#     router.root(Event('_input'))
#     router.root(Event('10000', 'a'))
#     result = services.results_service.get_current(os.environ["TEST_ROOM_ID"])
#     if not result.points == '{"a": 10000}':
#         errors.append("failed to input point")
#     router.root(Event('@b 20000', 'a'))
#     router.root(Event('60000', 'c'))
#     router.root(Event('@e 60000', 'c'))
#     router.root(Event('@e', 'c'))
#     router.root(Event('@c 30000', 'e'))
#     router.root(Event('@d 40000', 'd'))

#     # assert no error message has been registered, else print messages
#     assert not errors, "errors occured:\n{}".format("\n".join(errors))


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
