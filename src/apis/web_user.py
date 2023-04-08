# from typing import Dict, List
# from xml.dom import NotFoundErr
from flask import (
    Blueprint,
    request,
    render_template,
    session,
)
# from db_setting import Engine, Session
from ApplicationModels.PageContents import PageContents, RegisterFormData, ViewUserInfoData
from use_cases.web.ViewRegisterUseCase import ViewRegisterUseCase
from use_cases.web.ViewUserInfoUseCase import ViewUserInfoUseCase
from use_cases.web.RegisterWebUserUseCase import RegisterWebUserUseCase


web_user_blueprint = Blueprint('web_user_blueprint', __name__, url_prefix='/web_user')


@web_user_blueprint.route('/register', methods=['GET'])
def view_register():
    page_contents = PageContents[RegisterFormData](
        session, request, RegisterFormData)
    page_contents, forms = ViewRegisterUseCase().execute(
        page_contents=page_contents
    )
    return render_template(
        'register.html',
        page_contents=page_contents,
        form=forms
    )


@web_user_blueprint.route('/register', methods=['POST'])
def register():
    page_contents = PageContents(session, request)
    RegisterWebUserUseCase().execute(page_contents=page_contents)
    return render_template(
        'index.html',
        page_contents=page_contents,
    )


@web_user_blueprint.route('/user_info', methods=['GET'])
def view_user_info():
    page_contents = PageContents[ViewUserInfoData](session, request, ViewUserInfoData)
    page_contents = ViewUserInfoUseCase().execute(page_contents=page_contents)
    return render_template(
        'user_info.html',
        page_contents=page_contents,
    )
