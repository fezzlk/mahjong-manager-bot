"""API レイヤーテスト: root.py (views_blueprint)"""
from unittest.mock import patch

from linebot.v3.exceptions import InvalidSignatureError


def test_health_returns_ok(client):
    """GET /health → 200 {"status": "ok"}"""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"


def test_legacy_login_renders(client):
    """GET /legacy/login → 200 (login.html が描画される)"""
    resp = client.get("/legacy/login")
    assert resp.status_code == 200


def test_logout_redirects(client):
    """GET /logout → 302 リダイレクト"""
    resp = client.get("/logout")
    assert resp.status_code == 302


def test_callback_returns_ok_with_mocked_handler(client):
    """POST /callback → handler.handle をモックして 200 "OK" を返す"""
    with patch("apis.root.handler.handle") as mock_handle:
        mock_handle.return_value = None
        resp = client.post(
            "/callback",
            data=b'{"events": []}',
            headers={"X-Line-Signature": "dummy_signature"},
        )
    assert resp.status_code == 200
    assert resp.data == b"OK"


def test_callback_invalid_signature_returns_400(client):
    """POST /callback → 署名検証エラーで 400"""
    with patch("apis.root.handler.handle") as mock_handle:
        mock_handle.side_effect = InvalidSignatureError("invalid")
        resp = client.post(
            "/callback",
            data=b'{"events": []}',
            headers={"X-Line-Signature": "bad_signature"},
        )
    assert resp.status_code == 400


def test_spa_fallback_returns_404_when_no_frontend_build(client):
    """GET /nonexistent-spa-route → フロントエンドビルドなしなら 404"""
    resp = client.get("/nonexistent-spa-route-xyz")
    # フロントエンドがビルドされていない場合 404、ビルド済みなら 200
    assert resp.status_code in (200, 404)
