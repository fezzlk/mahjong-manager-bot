# Auth
from flask import (
    Blueprint,
    url_for,
    redirect,
    session,
    request,
    make_response,
    jsonify,
)
from oauth_client import oauth
from db_setting import Session
from DomainModel.entities.WebUser import WebUser
from repositories import web_user_repository
from linebot import WebhookHandler
import env_var
from flask_bcrypt import Bcrypt
from repositories import user_repository, session_scope

handler = WebhookHandler(env_var.YOUR_CHANNEL_SECRET)
auth_blueprint = Blueprint('auth_blueprint', __name__, url_prefix='/auth')


@auth_blueprint.route('/login', methods=['POST'])
def api_login():
    bcrypt = Bcrypt()
    user_id = request.args.get('user_id')
    password = request.args.get('password')
    bcrypt.check_password_hash(password, 'password')
    access_token = authenticate(line_user_id=user_id)
    response_body = {'access_token': access_token}
    return make_response(jsonify(response_body), 200)


def authenticate(line_user_id: str) -> str:
    with session_scope() as session:
        user = user_repository.find_one_by_line_user_id(
            session, line_user_id=line_user_id)
        if user is None:
            raise ValueError('ユーザーがいないか、複数存在します。')
        return create_access_token(identity=user.line_user_id)


@ auth_blueprint.route('/login/google')
def login_google():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth_blueprint.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@ auth_blueprint.route('/authorize')
def authorize():
    # 認証
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()

    # ユーザ検索
    db_session = Session()
    email = user_info['email']
    web_user = web_user_repository.find_one_by_email(session=db_session, email=email)

    # ヒットしない場合は新規登録画面
    if web_user is None:
        session['login_email'] = email
        session['login_name'] = user_info['name']
        new_webuser = WebUser(
            user_code=email,
            name=user_info['name'],
            email=email,
        )
        web_user = web_user_repository.create(session=db_session, new_webuser=new_webuser)
    
    # ヒットした場合はログイン
    session['login_picture'] = user_info['picture']
    session['access_token'] = token['access_token']
    session['id_token'] = token['id_token']
    session['login_user'] = web_user

    redirect_to = session.pop('next_page_url', '/')
    return redirect(redirect_to)


@ auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views_blueprint.index', message='ログアウトしました'))
