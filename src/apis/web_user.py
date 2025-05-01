# from typing import Dict, List
# from xml.dom import NotFoundErr
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# from db_setting import Engine, Session
from ApplicationModels.PageContents import (
    PageContents,
    RegisterFormData,
    ViewUserInfoData,
)
from middlewares import login_required
from use_cases.web.RegisterWebUserUseCase import RegisterWebUserUseCase
from use_cases.web.ViewRegisterUseCase import ViewRegisterUseCase
from use_cases.web.ViewUserInfoUseCase import ViewUserInfoUseCase

web_user_blueprint = Blueprint("web_user_blueprint", __name__, url_prefix="/web_user")


@web_user_blueprint.route("/register", methods=["GET"])
def view_register():
    page_contents = PageContents[RegisterFormData](
        session, request, RegisterFormData)
    page_contents, forms = ViewRegisterUseCase().execute(
        page_contents=page_contents,
    )
    return render_template(
        "register.html",
        page_contents=page_contents,
        form=forms,
    )


@web_user_blueprint.route("/register", methods=["POST"])
def register():
    page_contents = PageContents(session, request)
    RegisterWebUserUseCase().execute(page_contents=page_contents)
    return redirect(url_for(
        "views_blueprint.view_login",
        message=page_contents.message,
    ))


@web_user_blueprint.route("/me", methods=["GET"])
@login_required
def view_me():
    page_contents = PageContents[ViewUserInfoData](session, request, ViewUserInfoData)
    page_contents = ViewUserInfoUseCase().execute(page_contents=page_contents)
    return render_template(
        "me.html",
        page_contents=page_contents,
    )


@web_user_blueprint.route("/me/generate_api_token", methods=["POST"])
@login_required
def generate_api_token():
    user_id = session.get("login_user_id", None)
    if user_id is None:
        raise Exception("システムエラーが発生しました。")
    from flask_jwt_extended import create_access_token
    return "Bearer " + create_access_token(identity=user_id)
