"""システムテスト共通フィクスチャ
"""
import pytest

import server


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    return server.app.test_client()
