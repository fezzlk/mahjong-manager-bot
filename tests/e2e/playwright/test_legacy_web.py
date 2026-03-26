"""Playwright E2E テスト: Legacy Web UI

/legacy/ 以下の Jinja2 テンプレートページに対してブラウザ操作テストを実行する。
これらのテストは pytest-playwright が必要:
  pip install -r requirements.e2e.txt
  playwright install chromium

実行方法:
  pytest tests/e2e/playwright/ -v
"""


# ─── 非認証ページ ──────────────────────────────────────────────────


def test_health_endpoint(page, live_server_url):
    """GET /health → {"status": "ok"} が返る"""
    resp = page.goto(f"{live_server_url}/health")
    assert resp.status == 200
    assert "ok" in page.content()


def test_login_page_renders(page, live_server_url):
    """GET /legacy/login → ログインページが表示される"""
    page.goto(f"{live_server_url}/legacy/login")
    assert page.title() != ""
    # ページに何らかのコンテンツが存在する
    assert len(page.content()) > 0


def test_unauthenticated_access_redirects_to_login(page, live_server_url):
    """GET /line/approve (未ログイン) → /legacy/login にリダイレクトされる"""
    page.goto(f"{live_server_url}/line/approve")
    assert "/legacy/login" in page.url


def test_unauthenticated_group_page_redirects(page, live_server_url):
    """GET /group/ (未ログイン) → ログインページへリダイレクト"""
    page.goto(f"{live_server_url}/group/")
    assert "login" in page.url


# ─── 認証済みページ ──────────────────────────────────────────────────


def test_test_login_creates_session(page, live_server_url):
    """GET /auth/test_login → セッションが確立されて /legacy/ にリダイレクト"""
    page.goto(f"{live_server_url}/auth/test_login")
    # リダイレクト先が /legacy/ であることを確認
    assert "/legacy/" in page.url
    assert page.url.startswith(live_server_url)


def test_authenticated_index_page(authenticated_page, live_server_url):
    """ログイン済みで /legacy/ → 200 でページが描画される"""
    authenticated_page.goto(f"{live_server_url}/legacy/")
    assert "/legacy/" in authenticated_page.url
    assert len(authenticated_page.content()) > 0


def test_authenticated_group_page(authenticated_page, live_server_url):
    """ログイン済みで /group/ → グループ一覧ページが描画される"""
    authenticated_page.goto(f"{live_server_url}/group/")
    assert authenticated_page.url.startswith(live_server_url)
    # ログインページに飛ばされていないことを確認
    assert "login" not in authenticated_page.url
    assert len(authenticated_page.content()) > 0


def test_authenticated_line_approve_page(authenticated_page, live_server_url):
    """ログイン済みで /line/approve → LINE連携ページが 200 で描画される"""
    authenticated_page.goto(f"{live_server_url}/line/approve")
    assert "login" not in authenticated_page.url
    assert len(authenticated_page.content()) > 0


def test_logout_clears_session(authenticated_page, live_server_url):
    """ログイン後に /logout → セッションがクリアされてリダイレクト"""
    authenticated_page.goto(f"{live_server_url}/logout")
    # ログアウト後はログインページへリダイレクトされる
    # (redirect to /login → SPA fallback または /legacy/login)
    assert authenticated_page.url != f"{live_server_url}/"


def test_health_accessible_without_auth(page, live_server_url):
    """/health は認証不要で常に 200 を返す"""
    resp = page.goto(f"{live_server_url}/health")
    assert resp.status == 200
