
# import sys
# import os
# sys.path.append(os.path.abspath(".."))
from router import Router
from services import Services


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
