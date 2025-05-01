from functools import wraps

from flask import redirect, request, session, url_for

# from flask_jwt_extended import get_jwt_identity
from repositories import web_user_repository


def login_required(f):
    @wraps(f)
    def decorated_login_required(*args, **kwargs):
        session["next_page_url"] = request.url

        # セッションの login_user_id が未設定の場合はログイン画面に遷移
        login_user_id = session.get("login_user_id", None)
        if login_user_id is None:
            return redirect(
                url_for(
                    "views_blueprint.view_login",
                    next=request.url,
                ),
            )

        web_users = web_user_repository.find(
            query={
                "_id": login_user_id,
            },
        )

        # login_user_id に id が一致する web user がいなければ新規作成画面に遷移
        if len(web_users) == 0:
            return redirect(
                url_for(
                    "views_blueprint.view_login",
                    next=request.url,
                ),
            )

        session.pop("next_page_url", None)

        return f(*args, **kwargs)

    return decorated_login_required


def parse_jwt_token(f):
    @wraps(f)
    def decorated_parse_jwt_token(*args, **kwargs):
        # web_users = web_user_repository.find(
        #     query={
        #         "_id": get_jwt_identity(),
        #     },
        # )

        return f(*args, **kwargs)

    return decorated_parse_jwt_token
