# Auth
import requests
from flask import (
    Blueprint,
    abort,
    jsonify,
    make_response,
    redirect,
    request,
    session,
    url_for,
)
from flask_jwt_extended import create_access_token
from linebot.v3.webhook import WebhookHandler

import env_var
from extensions import limiter
from oauth_client import oauth
from repositories import user_repository, web_user_repository

handler = WebhookHandler(env_var.YOUR_CHANNEL_SECRET)
auth_blueprint = Blueprint("auth_blueprint", __name__, url_prefix="/auth")


@auth_blueprint.route("/login", methods=["POST"])
@limiter.limit("10/minute")
def api_login():
    # 本番環境ではパスワード認証なし /auth/login を無効化（LINE Login のみ使用）
    if env_var.FLASK_ENV == "production":
        abort(404)
    body = request.get_json(silent=True) or {}
    user_id = body.get("user_id")
    if not user_id:
        return make_response(jsonify({"error": "user_id is required"}), 400)
    try:
        access_token = authenticate(line_user_id=user_id)
    except ValueError:
        return make_response(jsonify({"error": "Unauthorized"}), 401)
    return make_response(jsonify({"access_token": access_token}), 200)


def authenticate(line_user_id: str) -> str:
    users = user_repository.find({"line_user_id": line_user_id})
    if len(users) == 0:
        raise ValueError("ユーザーがいないか、複数存在します。")
    return create_access_token(identity=users[0].line_user_id)


@auth_blueprint.route("/line/login")
@limiter.limit("10/minute")
def line_login():
    line = oauth.create_client("line")
    redirect_uri = url_for("auth_blueprint.line_authorize", _external=True)
    return line.authorize_redirect(redirect_uri)


@auth_blueprint.route("/line/authorize")
@limiter.limit("10/minute")
def line_authorize():
    line = oauth.create_client("line")
    token = line.authorize_access_token()

    # LINE Profile API でユーザー情報取得
    resp = requests.get(
        "https://api.line.me/v2/profile",
        headers={"Authorization": f"Bearer {token['access_token']}"},
        timeout=10,
    )
    resp.raise_for_status()
    profile = resp.json()
    line_user_id = profile["userId"]
    display_name = profile.get("displayName", "")

    # linked_line_user_id で web_users を検索
    web_users = web_user_repository.find(
        {"linked_line_user_id": line_user_id},
    )

    # ヒットしない場合は新規登録画面
    if len(web_users) == 0:
        session["login_line_user_id"] = line_user_id
        session["login_name"] = display_name
        return redirect(
            url_for("web_user_blueprint.view_register", _external=True),
        )

    # ヒットした場合はログイン
    web_user = web_users[0]
    session["access_token"] = token["access_token"]
    session["login_user_id"] = web_user._id

    # JWT を発行してフロントエンドへ渡す。ブラウザ履歴・Referrer・アクセスログへの
    # 平文JWT漏洩を避けるため、URLクエリではなく短命(60秒)のhttpOnly Cookieで
    # 一度だけ橋渡しする。SPA は起動時に GET /api/v1/auth/exchange でこの
    # Cookie を読み取り、以後は通常どおり Authorization ヘッダーで認証する。
    jwt_token = create_access_token(identity=str(web_user._id))
    redirect_to = session.pop("next_page_url", "/")
    response = make_response(redirect(redirect_to))
    response.set_cookie(
        "pending_token",
        jwt_token,
        max_age=60,
        httponly=True,
        secure=env_var.FLASK_ENV == "production",
        samesite="Lax",
    )
    return response
