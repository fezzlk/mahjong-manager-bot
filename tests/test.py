
# import sys
# import os
# sys.path.append(os.path.abspath(".."))
from services import Services
from router import Router
import os
print(os.environ["HOGE"])
print(os.environ["FUGA"])
print(os.environ["YOUR_CHANNEL_ACCESS_TOKEN"])


def init_test_dev():
    print('hoge')


def test_hoge():
    init_test_dev()
    a = 1
    b = 1
    assert a == b


def test_fuga():
    init_test_dev()
    a = 1
    b = 1
    Router.root()
    assert a == b
