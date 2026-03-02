"""API レイヤーテスト: auth.py (auth_blueprint)"""
from domain_model.entities.user import User
from repositories import user_repository


def test_login_success(client):
    """POST /auth/login (有効ユーザー) → 200 + access_token"""
    user = user_repository.create(
        User(line_user_id="U_auth_api_test_001", line_user_name="auth_test_user"),
    )
    resp = client.post(
        "/auth/login",
        json={"user_id": user.line_user_id},
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data


def test_login_user_not_found(client):
    """POST /auth/login (存在しないユーザー) → 401"""
    resp = client.post(
        "/auth/login",
        json={"user_id": "nonexistent_user_id_xyz"},
        content_type="application/json",
    )
    assert resp.status_code == 401
    data = resp.get_json()
    assert "Unauthorized" in data["error"]


def test_login_missing_user_id(client):
    """POST /auth/login (user_id なし) → 400"""
    resp = client.post(
        "/auth/login",
        json={},
        content_type="application/json",
    )
    assert resp.status_code == 400
    data = resp.get_json()
    assert "user_id is required" in data["error"]


def test_login_empty_body(client):
    """POST /auth/login (ボディなし) → 400"""
    resp = client.post(
        "/auth/login",
        content_type="application/json",
    )
    assert resp.status_code == 400
