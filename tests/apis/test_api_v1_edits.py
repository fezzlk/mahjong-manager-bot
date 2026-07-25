"""API レイヤーテスト: /api/v1/hanchans, /api/v1/matches (編集系エンドポイント)

Web UI からの素点・チップ修正、半荘・対戦削除のテスト。
"""
from domain_model.entities.group import Group
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match
from domain_model.entities.user_group import UserGroup
from domain_model.entities.user_hanchan import UserHanchan
from messaging_api_setting import line_bot_api
from mongo_client import audit_logs_collection
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
    user_group_repository,
    user_hanchan_repository,
)


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def _make_group_and_membership(line_group_id, line_user_id):
    group_repository.create(Group(line_group_id=line_group_id))
    user_group_repository.create(
        UserGroup(line_user_id=line_user_id, line_group_id=line_group_id),
    )


VALID_SCORES = {"U1": 40000, "U2": 30000, "U3": 20000, "U4": 10000}


def _make_match_with_hanchan(line_group_id, raw_scores=None):
    raw_scores = raw_scores or VALID_SCORES
    match = match_repository.create(Match(line_group_id=line_group_id))
    hanchan = hanchan_repository.create(
        Hanchan(line_group_id=line_group_id, match_id=match._id, raw_scores=raw_scores),
    )
    for i, (uid, score) in enumerate(
        sorted(raw_scores.items(), key=lambda x: x[1], reverse=True),
    ):
        user_hanchan_repository.create(
            UserHanchan(line_user_id=uid, hanchan_id=hanchan._id, point=score, rank=i + 1),
        )
    return match, hanchan


# ─── DELETE /api/v1/hanchans/<id> ──────────────────────────────

def test_delete_hanchan_without_token_returns_401(client):
    resp = client.delete("/api/v1/hanchans/000000000000000000000000")
    assert resp.status_code == 401


def test_delete_hanchan_returns_404_for_invalid_id(jwt_authenticated_client):
    client, token, _web_user, _line_user = jwt_authenticated_client
    resp = client.delete("/api/v1/hanchans/not-an-object-id", headers=_auth(token))
    assert resp.status_code == 404


def test_delete_hanchan_returns_403_when_not_member(jwt_authenticated_client, mocker):
    mocker.patch.object(line_bot_api, "push_message", return_value=None)
    client, token, _web_user, _line_user = jwt_authenticated_client
    line_group_id = "G_edits_delete_hanchan_403_0001"
    group_repository.create(Group(line_group_id=line_group_id))
    _match, hanchan = _make_match_with_hanchan(line_group_id)
    # メンバー登録はしない

    resp = client.delete(f"/api/v1/hanchans/{hanchan._id}", headers=_auth(token))
    assert resp.status_code == 403


def test_delete_hanchan_marks_deleted_and_recalculates_sum(jwt_authenticated_client, mocker):
    mock_push = mocker.patch.object(line_bot_api, "push_message", return_value=None)
    client, token, _web_user, line_user = jwt_authenticated_client
    line_group_id = "G_edits_delete_hanchan_ok_0001"
    _make_group_and_membership(line_group_id, line_user.line_user_id)
    match, hanchan = _make_match_with_hanchan(line_group_id)

    resp = client.delete(f"/api/v1/hanchans/{hanchan._id}", headers=_auth(token))
    assert resp.status_code == 200

    updated_hanchan = hanchan_repository.find({"_id": hanchan._id})
    assert updated_hanchan == []  # is_deleted な半荘はデフォルトの find で除外される

    remaining_user_hanchans = user_hanchan_repository.find({"hanchan_id": hanchan._id})
    assert remaining_user_hanchans == []

    updated_match = match_repository.find({"_id": match._id})[0]
    assert updated_match.sum_scores == {}

    assert mock_push.call_count == 1
    assert audit_logs_collection.count_documents({"action": "delete_hanchan"}) == 1


# ─── PUT /api/v1/hanchans/<id>/scores ──────────────────────────

def test_update_scores_without_token_returns_401(client):
    resp = client.put("/api/v1/hanchans/000000000000000000000000/scores", json={})
    assert resp.status_code == 401


def test_update_scores_returns_400_when_total_is_invalid(jwt_authenticated_client, mocker):
    mocker.patch.object(line_bot_api, "push_message", return_value=None)
    client, token, _web_user, line_user = jwt_authenticated_client
    line_group_id = "G_edits_update_scores_bad_total_01"
    _make_group_and_membership(line_group_id, line_user.line_user_id)
    _match, hanchan = _make_match_with_hanchan(line_group_id)

    bad_scores = {"U1": 40000, "U2": 30000, "U3": 20000, "U4": 5000}  # 合計95000
    resp = client.put(
        f"/api/v1/hanchans/{hanchan._id}/scores",
        json={"raw_scores": bad_scores},
        headers=_auth(token),
    )
    assert resp.status_code == 400


def test_update_scores_returns_400_when_tied(jwt_authenticated_client, mocker):
    mocker.patch.object(line_bot_api, "push_message", return_value=None)
    client, token, _web_user, line_user = jwt_authenticated_client
    line_group_id = "G_edits_update_scores_tied_0001"
    _make_group_and_membership(line_group_id, line_user.line_user_id)
    _match, hanchan = _make_match_with_hanchan(line_group_id)

    tied_scores = {"U1": 25000, "U2": 25000, "U3": 25000, "U4": 25000}
    resp = client.put(
        f"/api/v1/hanchans/{hanchan._id}/scores",
        json={"raw_scores": tied_scores},
        headers=_auth(token),
    )
    assert resp.status_code == 400


def test_update_scores_updates_hanchan_and_match_sum(jwt_authenticated_client, mocker):
    mock_push = mocker.patch.object(line_bot_api, "push_message", return_value=None)
    client, token, _web_user, line_user = jwt_authenticated_client
    line_group_id = "G_edits_update_scores_ok_00001"
    _make_group_and_membership(line_group_id, line_user.line_user_id)
    match, hanchan = _make_match_with_hanchan(line_group_id)

    new_scores = {"U1": 50000, "U2": 30000, "U3": 15000, "U4": 5000}
    resp = client.put(
        f"/api/v1/hanchans/{hanchan._id}/scores",
        json={"raw_scores": new_scores},
        headers=_auth(token),
    )
    assert resp.status_code == 200

    updated_hanchan = hanchan_repository.find({"_id": hanchan._id})[0]
    assert updated_hanchan.raw_scores == new_scores

    updated_match = match_repository.find({"_id": match._id})[0]
    assert updated_match.sum_scores == updated_hanchan.converted_scores

    assert mock_push.call_count == 1
    assert audit_logs_collection.count_documents({"action": "update_hanchan_scores"}) == 1


# ─── DELETE /api/v1/matches/<id> ───────────────────────────────

def test_delete_match_returns_404_for_invalid_id(jwt_authenticated_client):
    client, token, _web_user, _line_user = jwt_authenticated_client
    resp = client.delete("/api/v1/matches/not-an-object-id", headers=_auth(token))
    assert resp.status_code == 404


def test_delete_match_marks_match_and_hanchans_deleted(jwt_authenticated_client, mocker):
    mock_push = mocker.patch.object(line_bot_api, "push_message", return_value=None)
    client, token, _web_user, line_user = jwt_authenticated_client
    line_group_id = "G_edits_delete_match_ok_000001"
    _make_group_and_membership(line_group_id, line_user.line_user_id)
    match, hanchan = _make_match_with_hanchan(line_group_id)

    resp = client.delete(f"/api/v1/matches/{match._id}", headers=_auth(token))
    assert resp.status_code == 200

    assert match_repository.find({"_id": match._id}) == []
    assert hanchan_repository.find({"_id": hanchan._id}) == []

    assert mock_push.call_count == 1
    assert audit_logs_collection.count_documents({"action": "delete_match"}) == 1


# ─── PUT /api/v1/matches/<id>/chips ────────────────────────────

def test_update_chips_returns_403_when_not_member(jwt_authenticated_client, mocker):
    mocker.patch.object(line_bot_api, "push_message", return_value=None)
    client, token, _web_user, _line_user = jwt_authenticated_client
    line_group_id = "G_edits_update_chips_403_00001"
    match = match_repository.create(Match(line_group_id=line_group_id))
    # メンバー登録はしない

    resp = client.put(
        f"/api/v1/matches/{match._id}/chips",
        json={"chip_scores": {"U1": 5}},
        headers=_auth(token),
    )
    assert resp.status_code == 403


def test_update_chips_updates_match(jwt_authenticated_client, mocker):
    mock_push = mocker.patch.object(line_bot_api, "push_message", return_value=None)
    client, token, _web_user, line_user = jwt_authenticated_client
    line_group_id = "G_edits_update_chips_ok_000001"
    _make_group_and_membership(line_group_id, line_user.line_user_id)
    match = match_repository.create(Match(line_group_id=line_group_id))

    new_chips = {"U1": 5, "U2": -5}
    resp = client.put(
        f"/api/v1/matches/{match._id}/chips",
        json={"chip_scores": new_chips},
        headers=_auth(token),
    )
    assert resp.status_code == 200

    updated_match = match_repository.find({"_id": match._id})[0]
    assert updated_match.chip_scores == new_chips

    assert mock_push.call_count == 1
    assert audit_logs_collection.count_documents({"action": "update_chips"}) == 1
