"""シナリオテスト: LINE OAuth初回ログイン → 新規登録 → グループAPI認可

FEZ-59/60対応。旧「メール連携申請→Web承認」フローを廃止し、LINE OAuth
ログイン時点で自動リンクする方式に置き換えたことを検証する。
未登録のLINEユーザーがOAuthログイン(セッションにlogin_line_user_idが
入る)し、登録フォームを送信すると、承認ステップなしで即座に
linked_line_user_idがセットされ、そのままグループAPIの認可
(assert_group_member)を通過できることを確認する。
"""

from flask import Flask, request, session

from apis.api._auth import assert_group_member
from application_models.page_contents import PageContents
from domain_model.entities.user_group import UserGroup
from repositories import user_group_repository, web_user_repository
from use_cases.web.register_web_user_use_case import RegisterWebUserUseCase

LINE_GROUP_ID = "G_scenario_oauth_link_001_abc"

_app = Flask(__name__)
_app.secret_key = "test-secret"


def _register_via_oauth(login_line_user_id: str, email: str, name: str):
    """OAuthログイン直後(未登録)の状態から登録フォーム送信までを再現する。"""
    with _app.test_request_context(
        "/",
        method="POST",
        data={"name": name, "email": email},
    ):
        session["login_line_user_id"] = login_line_user_id
        page_contents = PageContents(session=session, request=request)
        RegisterWebUserUseCase().execute(page_contents)

    return web_user_repository.find({"user_code": email})[0]


def test_web_oauth_auto_link_flow():
    """OAuth自動リンクフロー。

    1. LINE OAuthログインで未登録と判定され、session に login_line_user_id が入る
    2. 登録フォームを送信すると、承認ステップなしで WebUser.linked_line_user_id が
       セットされる
    3. そのユーザーが対象グループのメンバーとして登録されていれば、
       assert_group_member が None (認可OK) を返す
    """
    line_user_id = "U_scenario_oauth_link_001_abcdefgh"
    email = "scenario_oauth_link_test@example.com"

    web_user = _register_via_oauth(line_user_id, email, "scenario_test_user")
    assert web_user.linked_line_user_id == line_user_id

    # === グループメンバーとして登録済みならAPI認可を通過する ===
    user_group_repository.create(
        UserGroup(line_user_id=line_user_id, line_group_id=LINE_GROUP_ID),
    )

    with _app.app_context():
        assert assert_group_member(web_user, LINE_GROUP_ID) is None


def test_web_oauth_auto_link_flow_rejects_non_member():
    """登録は完了していても、対象グループのメンバーでなければ403相当を返す。"""
    line_user_id = "U_scenario_oauth_link_002_abcdefgh"
    email = "scenario_oauth_link_test_2@example.com"

    web_user = _register_via_oauth(line_user_id, email, "scenario_test_user_2")

    with _app.app_context():
        response = assert_group_member(web_user, LINE_GROUP_ID)
        assert response is not None
        assert response.status_code == 403
