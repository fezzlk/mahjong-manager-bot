from datetime import timedelta

from flask import Flask, jsonify, make_response
from flask_jwt_extended import JWTManager

from repositories import user_repository


def identity(payload):
    user_id = payload["identity"]
    users = user_repository.find({"line_user_id": user_id})
    if len(users) != 1:
        raise ValueError("ユーザーが取得できません")
    return users[0]


def register_jwt(app: Flask):
    #     # Flask JWT
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_ALGORITHM"] = "HS256"                       # 暗号化署名のアルゴリズム
    app.config["JWT_LEEWAY"] = 0                                # 有効期限に対する余裕時間
    app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=600)  # トークンの有効期間
    app.config["JWT_NOT_BEFORE_DELTA"] = timedelta(
        seconds=0)   # トークンの使用を開始する相対時間

    jwt = JWTManager(app)
    jwt.unauthorized_loader(jwt_unauthorized_loader_handler)


def jwt_unauthorized_loader_handler(reason):
    print(reason)
    return make_response(jsonify({"error": "Unauthorized"}), 401)
