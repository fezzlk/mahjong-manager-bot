"""Playwright E2E テスト共通フィクスチャ

Flask アプリをバックグラウンドスレッドで起動し、
実ブラウザからアクセスするためのライブサーバー URL を提供する。
"""
import socket
import threading
import time

import pytest

# パスは tests/conftest.py で設定済みなので import 可能
import server

_SERVER_PORT = 5099
_BASE_URL = f"http://localhost:{_SERVER_PORT}"


@pytest.fixture(scope="session")
def live_server_url():
    """Flask をバックグラウンドスレッドで起動し、URL を返す。"""
    server.app.config["TESTING"] = True
    server.app.config["SERVER_NAME"] = None  # allow any host

    thread = threading.Thread(
        target=lambda: server.app.run(
            host="127.0.0.1",
            port=_SERVER_PORT,
            use_reloader=False,
            threaded=True,
        ),
        daemon=True,
    )
    thread.start()

    # サーバーが起動するまで待機
    for _ in range(30):
        try:
            with socket.create_connection(("127.0.0.1", _SERVER_PORT), timeout=0.5):
                break
        except OSError:
            time.sleep(0.2)

    return _BASE_URL


@pytest.fixture
def base_url(live_server_url):
    return live_server_url


@pytest.fixture
def authenticated_page(page, live_server_url):
    """ログイン済み状態のブラウザページを返す。

    /auth/test_login エンドポイントを通じてセッションを確立する。
    """
    page.goto(f"{live_server_url}/auth/test_login")
    return page
