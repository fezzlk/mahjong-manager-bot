"""API レイヤーテスト: GET /api/v1/auth/exchange

LINE Login コールバック直後に一度だけ Cookie へ橋渡しした JWT を SPA へ渡すエンドポイント。
"""
from flask_jwt_extended import create_access_token

import server as srv
from domain_model.entities.web_user import WebUser
from repositories import web_user_repository


def test_exchange_without_cookie_returns_204(client):
    resp = client.get("/api/v1/auth/exchange")
    assert resp.status_code == 204


def test_exchange_with_cookie_returns_token_and_clears_cookie(client):
    web_user = web_user_repository.create(
        WebUser(user_code="exchange@example.com", name="Exchange User"),
    )
    with srv.app.app_context():
        token = create_access_token(identity=str(web_user._id))

    client.set_cookie("pending_token", token)
    resp = client.get("/api/v1/auth/exchange")

    assert resp.status_code == 200
    assert resp.get_json()["access_token"] == token

    set_cookie_header = resp.headers.get("Set-Cookie", "")
    assert "pending_token=" in set_cookie_header
    assert "Max-Age=0" in set_cookie_header


def test_exchange_cannot_be_reused(client):
    web_user = web_user_repository.create(
        WebUser(user_code="exchange2@example.com", name="Exchange User 2"),
    )
    with srv.app.app_context():
        token = create_access_token(identity=str(web_user._id))

    client.set_cookie("pending_token", token)
    first = client.get("/api/v1/auth/exchange")
    assert first.status_code == 200

    second = client.get("/api/v1/auth/exchange")
    assert second.status_code == 204
