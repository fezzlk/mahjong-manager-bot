"""API認証ヘルパー: JWT から WebUser を取得するデコレータ"""
import functools
from typing import Callable

from bson.objectid import ObjectId
from flask import jsonify, make_response
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from repositories import web_user_repository


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
