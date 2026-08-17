"""API レイヤーテスト: GET /api/v1/matches/<id> (対戦詳細)"""
from domain_model.entities.group import Group
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match
from domain_model.entities.user_group import UserGroup
from domain_model.entities.user_hanchan import UserHanchan
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
    user_group_repository,
    user_hanchan_repository,
)


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


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


def test_get_match_without_token_returns_401(client):
    resp = client.get("/api/v1/matches/000000000000000000000000")
    assert resp.status_code == 401


def test_get_match_returns_404_for_invalid_id(jwt_authenticated_client):
    client, token, _web_user, _line_user = jwt_authenticated_client
    resp = client.get("/api/v1/matches/not-an-object-id", headers=_auth(token))
    assert resp.status_code == 404


def test_get_match_returns_403_when_not_member(jwt_authenticated_client):
    client, token, _web_user, _line_user = jwt_authenticated_client
    line_group_id = "G_matches_get_403_not_member_01"
    group_repository.create(Group(line_group_id=line_group_id))
    match, _hanchan = _make_match_with_hanchan(line_group_id)
    # メンバー登録はしない

    resp = client.get(f"/api/v1/matches/{match._id}", headers=_auth(token))
    assert resp.status_code == 403


def test_get_match_returns_200_for_own_group_member(jwt_authenticated_client):
    client, token, _web_user, line_user = jwt_authenticated_client
    line_group_id = "G_matches_get_200_own_group_001"
    group_repository.create(Group(line_group_id=line_group_id))
    user_group_repository.create(
        UserGroup(line_user_id=line_user.line_user_id, line_group_id=line_group_id),
    )
    match, hanchan = _make_match_with_hanchan(line_group_id)

    resp = client.get(f"/api/v1/matches/{match._id}", headers=_auth(token))
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["id"] == str(match._id)
    assert len(body["hanchans"]) == 1
    assert body["hanchans"][0]["id"] == str(hanchan._id)


def test_get_match_allows_destination_group_member_after_merge(jwt_authenticated_client):
    """グループ統合(merged_into)後、統合先グループのメンバーは統合元グループ由来の
    対戦詳細を閲覧できることを確認する(FEZ-58、Codex review指摘)。

    一覧(GET /groups/<id>/matches)は統合チェーンを辿って統合元の対戦も表示するが、
    詳細側の認可が対戦自身のline_group_id(統合元)のみを見ていたため、統合先の
    メンバーが一覧から辿ると403になっていた。
    """
    client, token, _web_user, line_user = jwt_authenticated_client
    source_group_id = "G_matches_merge_src_00000001"
    destination_group_id = "G_matches_merge_dst_00000001"
    group_repository.create(Group(line_group_id=source_group_id))
    group_repository.create(Group(line_group_id=destination_group_id))
    group_repository.update(
        {"line_group_id": source_group_id},
        {"merged_into": destination_group_id},
    )
    # line_userは統合先グループにのみ所属(統合元へのメンバーシップは引き継がれない)
    user_group_repository.create(
        UserGroup(line_user_id=line_user.line_user_id, line_group_id=destination_group_id),
    )
    match, _hanchan = _make_match_with_hanchan(source_group_id)

    resp = client.get(f"/api/v1/matches/{match._id}", headers=_auth(token))
    assert resp.status_code == 200
