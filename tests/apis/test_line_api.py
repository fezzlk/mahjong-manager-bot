"""API レイヤーテスト: line.py (line_blueprint) — login_required デコレータ含む"""


def test_view_approve_without_auth_redirects_to_login(client):
    """GET /line/approve (未ログイン) → 302 → /legacy/login"""
    resp = client.get("/line/approve")
    assert resp.status_code == 302
    assert "/legacy/login" in resp.headers["Location"]


def test_view_approve_with_auth_returns_200(authenticated_client):
    """GET /line/approve (ログイン済み) → 200"""
    resp = authenticated_client.get("/line/approve")
    assert resp.status_code == 200


def test_approve_post_without_auth_redirects(client):
    """POST /line/approve (未ログイン) → 302"""
    resp = client.post("/line/approve")
    assert resp.status_code == 302
    assert "/legacy/login" in resp.headers["Location"]


def test_deny_post_without_auth_redirects(client):
    """POST /line/deny (未ログイン) → 302"""
    resp = client.post("/line/deny")
    assert resp.status_code == 302
    assert "/legacy/login" in resp.headers["Location"]


def test_release_post_without_auth_redirects(client):
    """POST /line/release (未ログイン) → 302"""
    resp = client.post("/line/release")
    assert resp.status_code == 302
    assert "/legacy/login" in resp.headers["Location"]
