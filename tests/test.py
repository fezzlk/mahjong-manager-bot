
import set_local_env  # for local dev env

from services import Services
from router import Router


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
    Router.root(event)
    assert a == b
