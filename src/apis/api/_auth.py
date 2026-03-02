"""API認証ヘルパー: JWT から WebUser を取得するデコレータ"""
import functools
from typing import Callable

from bson.objectid import ObjectId
from flask import jsonify, make_response
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from repositories import user_group_repository, web_user_repository


def require_web_user(f: Callable) -> Callable:
    """JWT を検証し、WebUser を取得してハンドラに渡す。

    デコレートされた関数の第1引数として `web_user` が渡される。
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return make_response(jsonify({"error": "Unauthorized"}), 401)

        identity = get_jwt_identity()
        try:
            web_users = web_user_repository.find({"_id": ObjectId(identity)})
        except Exception:
            return make_response(jsonify({"error": "Unauthorized"}), 401)

        if len(web_users) == 0:
            return make_response(jsonify({"error": "Unauthorized"}), 401)

        return f(web_users[0], *args, **kwargs)

    return wrapper


def assert_group_member(web_user, line_group_id: str):
    """web_user がグループのメンバーでなければ 403 レスポンスを返す。

    メンバーであれば None を返す。呼び出し元は戻り値が None でないときに
    そのまま return すること。
    """
    line_user_id = web_user.linked_line_user_id
    if not line_user_id:
        return make_response(jsonify({"error": "Forbidden"}), 403)
    members = user_group_repository.find({"line_group_id": line_group_id})
    if not any(m.line_user_id == line_user_id for m in members):
        return make_response(jsonify({"error": "Forbidden"}), 403)
    return None
