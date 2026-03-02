"""API レイヤーテスト: /api/v1/* (REST API — JWT 認証)

React フロントエンドが使う JWT 保護エンドポイントのテスト。
"""
from flask_jwt_extended import create_access_token

import server as srv
from domain_model.entities.group import Group
from domain_model.entities.user_group import UserGroup
from domain_model.entities.web_user import WebUser
from repositories import group_repository, user_group_repository, web_user_repository


def _auth(token):
    """Return Authorization header dict."""
    return {"Authorization": f"Bearer {token}"}


# ─── /api/v1/me ───────────────────────────────────────────────

def test_get_me_without_token_returns_401(client):
    """GET /api/v1/me (トークンなし) → 401"""
    resp = client.get("/api/v1/me")
    assert resp.status_code == 401


def test_get_me_with_token_returns_user_info(jwt_authenticated_client):
    """GET /api/v1/me (JWT 認証済み) → 200 + ユーザー情報"""
    client, token, web_user, line_user = jwt_authenticated_client
    resp = client.get("/api/v1/me", headers=_auth(token))
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["name"] == web_user.name
    assert data["email"] == web_user.email
    assert data["line_user_id"] == line_user.line_user_id


# ─── /api/v1/groups ───────────────────────────────────────────

def test_get_groups_returns_empty_when_no_groups(jwt_authenticated_client):
    """GET /api/v1/groups → LINE連携あるが所属グループなし → []"""
    client, token, _web_user, _line_user = jwt_authenticated_client
    resp = client.get("/api/v1/groups", headers=_auth(token))
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_get_groups_returns_groups(jwt_authenticated_client):
    """GET /api/v1/groups → グループに所属している場合 → 1件以上返る"""
    client, token, _web_user, line_user = jwt_authenticated_client
    line_group_id = "G_api_v1_test_group_001_abcde"

    group_repository.create(Group(line_group_id=line_group_id))
    user_group_repository.create(
        UserGroup(line_user_id=line_user.line_user_id, line_group_id=line_group_id),
    )

    resp = client.get("/api/v1/groups", headers=_auth(token))
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["name"] == line_group_id
    assert data[0]["member_count"] == 1


def test_get_groups_returns_empty_when_no_line_user(client):
    """GET /api/v1/groups → linked_line_user_id なし → []"""
    unlinked = web_user_repository.create(
        WebUser(
            user_code="unlinked@example.com",
            name="Unlinked User",
            linked_line_user_id=None,
        ),
    )
    with srv.app.app_context():
        token = create_access_token(identity=str(unlinked._id))

    resp = client.get("/api/v1/groups", headers=_auth(token))
    assert resp.status_code == 200
    assert resp.get_json() == []


# ─── /api/v1/groups/<group_id> ────────────────────────────────

def test_get_group_returns_404_for_invalid_id(jwt_authenticated_client):
    """GET /api/v1/groups/<invalid_id> → 404"""
    client, token, _web_user, _line_user = jwt_authenticated_client
    resp = client.get("/api/v1/groups/invalid_id", headers=_auth(token))
    assert resp.status_code == 404


def test_get_group_returns_403_when_not_member(jwt_authenticated_client):
    """GET /api/v1/groups/<id> → メンバーでない → 403"""
    client, token, _web_user, _line_user = jwt_authenticated_client
    line_group_id = "G_api_v1_not_member_001_abcde"

    group = group_repository.create(Group(line_group_id=line_group_id))
    # user_group は作らない (メンバーでない)

    resp = client.get(f"/api/v1/groups/{group._id}", headers=_auth(token))
    assert resp.status_code == 403


def test_get_group_returns_group_detail(jwt_authenticated_client):
    """GET /api/v1/groups/<id> → メンバーなら 200 + グループ詳細"""
    client, token, _web_user, line_user = jwt_authenticated_client
    line_group_id = "G_api_v1_detail_test_001_abcde"

    group = group_repository.create(Group(line_group_id=line_group_id))
    user_group_repository.create(
        UserGroup(line_user_id=line_user.line_user_id, line_group_id=line_group_id),
    )

    resp = client.get(f"/api/v1/groups/{group._id}", headers=_auth(token))
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == str(group._id)
    assert data["member_count"] == 1
    assert len(data["members"]) == 1
    assert data["members"][0]["line_user_id"] == line_user.line_user_id


# ─── /api/v1/groups/<group_id>/matches ────────────────────────

def test_get_matches_returns_empty_when_no_matches(jwt_authenticated_client):
    """GET /api/v1/groups/<id>/matches → マッチなし → []"""
    client, token, _web_user, line_user = jwt_authenticated_client
    line_group_id = "G_api_v1_matches_empty_001_abc"

    group = group_repository.create(Group(line_group_id=line_group_id))
    user_group_repository.create(
        UserGroup(line_user_id=line_user.line_user_id, line_group_id=line_group_id),
    )

    resp = client.get(f"/api/v1/groups/{group._id}/matches", headers=_auth(token))
    assert resp.status_code == 200
    assert resp.get_json() == []


# ─── /api/v1/groups/<group_id>/ranking ────────────────────────

def test_get_ranking_returns_empty_when_no_data(jwt_authenticated_client):
    """GET /api/v1/groups/<id>/ranking → データなし → []"""
    client, token, _web_user, line_user = jwt_authenticated_client
    line_group_id = "G_api_v1_ranking_empty_001_abc"

    group = group_repository.create(Group(line_group_id=line_group_id))
    user_group_repository.create(
        UserGroup(line_user_id=line_user.line_user_id, line_group_id=line_group_id),
    )

    resp = client.get(f"/api/v1/groups/{group._id}/ranking", headers=_auth(token))
    assert resp.status_code == 200
    assert resp.get_json() == []
