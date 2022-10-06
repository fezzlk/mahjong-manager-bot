# from flask import Flask
# from repositories import user_repository, session_scope
# from flask_jwt import JWT
# from werkzeug.security import safe_str_cmp
# from datetime import timedelta, datetime
# import env_var


# def authenticate(_id: str, line_user_id: str):
#     with session_scope() as session:
#         users = user_repository.find_by_ids(session, [int(_id)])
#         if len(users) != 1:
#             raise ValueError('ユーザーがいないか、複数存在します。')
#         user = users[0]
#         if safe_str_cmp(
#                 user.line_user_id.encode('utf-8'),
#                 line_user_id.encode('utf-8')):
#             return user


# def identity(payload):
#     with session_scope() as session:
#         user_id = payload['identity']
#         users = user_repository.find_by_ids(session, [user_id])
#         if len(users) != 1:
#             raise ValueError('ユーザーidが取得できません')
#         return users[0]


# def register_jwt(app: Flask):
#     # JSONのソートを抑止
#     app.config['SECRET_KEY'] = 'super-secret'
#     app.config['JSON_SORT_KEYS'] = False
#     # Flask JWT
#     app.config['JWT_ALGORITHM'] = 'HS256'                       # 暗号化署名のアルゴリズム
#     app.config['JWT_LEEWAY'] = 0                                # 有効期限に対する余裕時間
#     app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=300)  # トークンの有効期間
#     app.config['JWT_NOT_BEFORE_DELTA'] = timedelta(
#         seconds=0)   # トークンの使用を開始する相対時間
#     app.config['JWT_AUTH_URL_RULE'] = '/' + \
#         env_var.JWT_AUTH_PATH                   # 認証エンドポイントURL
#     # 認証エンドポイントURL
#     app.config['JWT_AUTH_USERNAME_KEY'] = '_id'
#     # 認証エンドポイントURL
#     app.config['JWT_AUTH_PASSWORD_KEY'] = 'line_user_id'

#     jwt = JWT(app, authenticate, identity)

#     @jwt.jwt_payload_handler
#     def make_payload(identity):
#         iat = datetime.utcnow()
#         exp = iat + app.config.get('JWT_EXPIRATION_DELTA')
#         nbf = iat + app.config.get('JWT_NOT_BEFORE_DELTA')
#         identity = getattr(identity, '_id')
#         return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}

#     return jwt
