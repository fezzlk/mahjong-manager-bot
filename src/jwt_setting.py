from flask import Flask
from repositories import user_repository, session_scope
from flask_jwt import JWT
from werkzeug.security import safe_str_cmp
from datetime import timedelta


def authenticate(line_user_name, line_user_id):
    with session_scope() as session:
        users = user_repository.find_by_name(session, line_user_name)
        if len(users) != 1:
            raise ValueError('ユーザーがいないか、複数存在します。')
        user = users[0]
        if safe_str_cmp(user.line_user_id.encode('utf-8'), line_user_id.encode('utf-8')):
            return user


def identity(payload):
    with session_scope() as session:
        user_id = payload['identity']
        users = user_repository.find_by_ids(session, [user_id])
        if len(users) != 1:
            raise ValueError('ユーザーidが取得できません')
        return users[0]


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


# def authenticate(line_user_name, password):
#     print('hoghogeg')
#     user = username_table.get(line_user_name, None)
#     if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
#         return user


# def identity(payload):
#     user_id = payload['identity']
#     return userid_table.get(user_id, None)



def register_jwt(app: Flask):
    # JSONのソートを抑止
    app.config['SECRET_KEY'] = 'super-secret'
    app.config['JSON_SORT_KEYS'] = False
    # Flask JWT
    app.config['JWT_ALGORITHM'] = 'HS256'                       # 暗号化署名のアルゴリズム
    app.config['JWT_LEEWAY'] = 0                                # 有効期限に対する余裕時間
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=300)  # トークンの有効期間
    app.config['JWT_NOT_BEFORE_DELTA'] = timedelta(seconds=0)   # トークンの使用を開始する相対時間
    app.config['JWT_AUTH_URL_RULE'] = '/auth'                   # 認証エンドポイントURL
    app.config['JWT_AUTH_USERNAME_KEY'] = 'line_user_name'                   # 認証エンドポイントURL
    app.config['JWT_AUTH_PASSWORD_KEY'] = 'line_user_id'                   # 認証エンドポイントURL

    return JWT(app, authenticate, identity)
