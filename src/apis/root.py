import os

from flask import (
    Blueprint,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from linebot.v3.exceptions import InvalidSignatureError

from application_models.page_contents import PageContents

# handle_eventからhandlerをインポート（イベントハンドラーが登録された状態）
from handle_event import handler

views_blueprint = Blueprint("views_blueprint", __name__, url_prefix="/")


@views_blueprint.route("/health")
def health():
    """Cloud Run ヘルスチェックエンドポイント"""
    return jsonify({"status": "ok"}), 200


@views_blueprint.route("/")
def index():
    page_contents = PageContents(session, request)
    if request.args.get("message") is not None:
        page_contents.message = request.args.get("message")
    return render_template("index.html", page_contents=page_contents)


@views_blueprint.route("/callback", methods=["POST"])
def callback():
    """Endpoint for LINE messaging API"""
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@views_blueprint.route("/uploads/<path:filename>")
def download_file(filename: str):
    return send_from_directory(
        "uploads/",
        filename,
        as_attachment=True,
    )


@views_blueprint.route("/login", methods=["GET"])
def view_login():
    page_contents = PageContents(session, request)
    return render_template(
        "login.html",
        page_contents=page_contents,
    )


@views_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("views_blueprint.view_login"))


@views_blueprint.route("/create_dummy", methods=["POST"])
def create_dummy():
    if os.environ.get("FLASK_ENV") == "production":
        abort(404)
    # Avoid importing test-only dummy dependencies at app startup.
    from use_cases.create_dummy_use_case import CreateDummyUseCase  # noqa: PLC0415

    CreateDummyUseCase().execute()
    return "Done"


@views_blueprint.route("/migrate", methods=["POST"])
def migrate():
    return "done"


@views_blueprint.route("/test_personal_line", methods=["POST"])
def test_personal_line():
    if os.environ.get("FLASK_ENV") == "production":
        abort(404)
    from application_service import (  # noqa: PLC0415
        reply_service,
        request_info_service,
    )
    from line_models import Event  # noqa: PLC0415

    user_id = request.form.get("user_id")
    text = request.form.get("text")
    event = Event(
        user_id=user_id,
        text=text,
    )
    request_info_service.set_req_info(event)
    import routing_by_text_in_personal_line  # noqa: PLC0415
    routing_by_text_in_personal_line.routing_by_text_in_personal_line()
    return "\n\n".join([content.text for content in reply_service.texts])
