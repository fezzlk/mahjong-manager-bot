# Auth
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from linebot import WebhookHandler

import env_var
from ApplicationModels.PageContents import PageContents
from middlewares import login_required
from use_cases.web.ApproveLinkLineUserUseCase import ApproveLinkLineUserUseCase
from use_cases.web.DenyLinkLineUserUseCase import DenyLinkLineUserUseCase
from use_cases.web.ReleaseLineUserUseCase import ReleaseLineUserUseCase
from use_cases.web.ViewApproveLinkLineUseCase import ViewApproveLinkLineUseCase

handler = WebhookHandler(env_var.YOUR_CHANNEL_SECRET)
line_blueprint = Blueprint("line_blueprint", __name__, url_prefix="/line")


@line_blueprint.route("/approve", methods=["GET"])
@login_required
def view_approve_link_line_user(message: str = ""):
    page_contents = PageContents(session, request)
    page_contents = ViewApproveLinkLineUseCase().execute(
        page_contents=page_contents,
    )

    page_contents.message = request.args.get("message", "")

    return render_template(
        "line_approve.html",
        page_contents=page_contents,
    )


@line_blueprint.route("/approve", methods=["POST"])
@login_required
def approve_line_user():
    page_contents = PageContents(session, request)
    ApproveLinkLineUserUseCase().execute(page_contents=page_contents)
    return redirect(url_for(
        "line_blueprint.view_approve_link_line_user",
        message=page_contents.message,
    ))


@line_blueprint.route("/release", methods=["POST"])
@login_required
def release_line_user():
    page_contents = PageContents(session, request)
    ReleaseLineUserUseCase().execute(page_contents=page_contents)
    return redirect(url_for(
        "line_blueprint.view_approve_link_line_user",
        message=page_contents.message,
    ))


@line_blueprint.route("/deny", methods=["POST"])
@login_required
def deny_line_user():
    page_contents = PageContents(session, request)
    DenyLinkLineUserUseCase().execute(page_contents=page_contents)
    return redirect(url_for(
        "line_blueprint.view_approve_link_line_user",
        message=page_contents.message,
    ))
