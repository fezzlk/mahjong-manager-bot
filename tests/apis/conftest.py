import pytest
from flask_jwt_extended import create_access_token

import server
from domain_model.entities.user import User
from domain_model.entities.web_user import WebUser
from repositories import user_repository, web_user_repository


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    return server.app.test_client()


@pytest.fixture
def jwt_authenticated_client(client):
    """JWT 認証済みクライアント (for /api/v1/* endpoints)。

    Returns: (client, token, web_user, line_user)
    """
    line_user = user_repository.create(
        User(line_user_id="U_jwt_api_test_001_abcdefghijkl", line_user_name="jwt_api_user"),
    )
    web_user = web_user_repository.create(
        WebUser(
            user_code="jwt_api@example.com",
            name="JWT API User",
            email="jwt_api@example.com",
            linked_line_user_id=line_user.line_user_id,
            is_approved_line_user=True,
        ),
    )
    with server.app.app_context():
        token = create_access_token(identity=str(web_user._id))
    return client, token, web_user, line_user


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
