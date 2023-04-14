from functools import wraps

from flask import request, redirect, url_for, session
from repositories import (
    web_user_repository, session_scope
)
from flask_jwt_extended import get_jwt_identity


def login_required(f):
    @wraps(f)
    def decorated_login_required(*args, **kwargs):
        session['next_page_url'] = request.url

        # メールアドレスがわからない(認証を通っていない)場合はログイン画面に遷移
        login_user_id = session.get('login_user_id', '')
        if login_user_id == '':
            return redirect(url_for(
                'views_blueprint.view_login', next=request.url
            ))

        with session_scope() as db_session:
            web_user = web_user_repository.find_by_id(
                session=db_session, id=login_user_id,
            )

            # メールアドレスが一致する web user がいなければ新規作成画面に遷移
            if web_user is None:
                return redirect(url_for(
                    'views_blueprint.view_login', next=request.url
                ))

        session.pop('next_page_url', None)

        return f(*args, **kwargs)

    return decorated_login_required


def parse_jwt_token(f):
    @wraps(f)
    def decorated_parse_jwt_token(*args, **kwargs):
        with session_scope() as db_session:
            web_user = web_user_repository.find_by_id(
                session=db_session, id=get_jwt_identity(),
            )

        return f(*args, **kwargs)

    return decorated_parse_jwt_token
