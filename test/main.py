from ..router import Router
from ..services import Services


def test_hoge():
    a = 1
    b = 1
    assert a == b


def test_fuga():
    a = 1
    b = 1
    Router.root()
    assert a == b
