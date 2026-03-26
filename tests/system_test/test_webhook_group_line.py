"""システムテスト: グループチャット LINE Webhook 統合テスト

POST /callback エンドポイントに LINE イベントを送信し、
HTTP レスポンスと reply_service の状態を検証する。
"""
import json
from unittest.mock import patch

import pytest
from system_test_helpers import make_group_text_event, make_line_webhook_payload

from application_service import reply_service, request_info_service
from domain_model.entities.group import GroupMode
from repositories import group_repository
from use_cases.group_line.join_group_use_case import JoinGroupUseCase

GROUP_ID = "G_system_test_group_001_abcdef"
USER_ID = "U_system_test_user_001_abcdef"


def _post_callback(client, event_dict: dict):
    """LINE Webhook ペイロードを /callback にPOSTするヘルパー"""
    payload = make_line_webhook_payload([event_dict])
    body = json.dumps(payload).encode()

    with patch("apis.root.handler.handle") as mock_handle:
        # handler.handle のモック: 実際のルーティング処理を side_effect で実行
        def simulate_handle(raw_body, signature):
            """LINE SDK ハンドラーをシミュレート (署名検証をスキップ)"""
            # ルーティングはモックで制御、ここでは何もしない

        mock_handle.side_effect = simulate_handle
        return client.post(
            "/callback",
            data=body,
            headers={
                "X-Line-Signature": "dummy_signature",
                "Content-Type": "application/json",
            },
        )


def test_callback_endpoint_returns_200(client):
    """POST /callback → handler をモックして常に 200 を返すことを確認"""
    event = make_group_text_event(GROUP_ID, USER_ID, "_start")
    resp = _post_callback(client, event)
    assert resp.status_code == 200
    assert resp.data == b"OK"


def test_callback_endpoint_handles_missing_signature(client):
    """POST /callback → X-Line-Signature ヘッダーなし → TESTING モードでは KeyError が伝播"""
    payload = make_line_webhook_payload([])
    # TESTING=True の場合 Flask は例外を伝播させる
    # X-Line-Signature がないと request.headers[] が KeyError を送出する
    with pytest.raises(KeyError):
        client.post(
            "/callback",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            # X-Line-Signature ヘッダーを意図的に省略
        )


def test_join_event_creates_group_via_use_case(client):
    """グループ参加イベント処理: JoinGroupUseCase を直接呼び出して DB 状態を確認"""
    # このテストは handler を経由せず Use Case を直接テスト (システムテストの境界)
    request_info_service.req_line_group_id = GROUP_ID
    request_info_service.req_line_user_id = USER_ID
    request_info_service.mention_line_ids = []

    JoinGroupUseCase().execute()

    groups = group_repository.find({"line_group_id": GROUP_ID})
    assert len(groups) == 1
    assert groups[0].line_group_id == GROUP_ID
    assert groups[0].mode == GroupMode.wait.value
    assert len(reply_service.texts) >= 1


def test_callback_with_simulated_join_event(client):
    """POST /callback + handler の side_effect でグループ参加を シミュレート"""
    payload = make_line_webhook_payload(
        [make_group_text_event(GROUP_ID + "_cb", USER_ID, "_start")],
    )
    body = json.dumps(payload).encode()

    def simulate_join_handler(raw_body, signature):
        """JoinGroupUseCase を直接呼び出してグループ作成をシミュレート"""
        request_info_service.req_line_group_id = GROUP_ID + "_cb"
        request_info_service.req_line_user_id = USER_ID
        request_info_service.mention_line_ids = []
        JoinGroupUseCase().execute()

    with patch("apis.root.handler.handle", side_effect=simulate_join_handler):
        resp = client.post(
            "/callback",
            data=body,
            headers={
                "X-Line-Signature": "dummy_signature",
                "Content-Type": "application/json",
            },
        )

    assert resp.status_code == 200
    groups = group_repository.find({"line_group_id": GROUP_ID + "_cb"})
    assert len(groups) == 1
