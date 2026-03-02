import pytest

import server
from domain_model.entities.web_user import WebUser
from repositories import web_user_repository


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    return server.app.test_client()


@pytest.fixture
def authenticated_client(client):
    """login_required を通過できる WebUser をDBに作成しセッションをセットする。

    Flask セッションクッキーは JSON シリアライズが必要なため、
    ObjectId を避けて整数の _id で WebUser を作成する。
    """
    # _id に整数を指定することで JSON シリアライズ可能にする
    web_user = web_user_repository.create(
        WebUser(user_code="test_auth", name="testuser", _id=9901),
    )
    with client.session_transaction() as sess:
        sess["login_user_id"] = web_user._id  # 整数なので JSON シリアライズ可能
    return client
