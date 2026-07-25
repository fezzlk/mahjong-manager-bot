from flask import jsonify, make_response, request

import env_var

from . import api_blueprint


@api_blueprint.route("/auth/exchange", methods=["GET"])
def exchange_pending_token():
    """LINE Login コールバック直後に一度だけ Cookie へ橋渡しした JWT を SPA へ渡す。

    `src/apis/auth.py` の `line_authorize` がセットする短命 Cookie (`pending_token`)
    を読み取り、JSON で返却しつつ即座に失効させる。Cookie が無ければ 204。
    """
    pending_token = request.cookies.get("pending_token")
    if not pending_token:
        return make_response("", 204)

    response = make_response(jsonify({"access_token": pending_token}), 200)
    response.set_cookie(
        "pending_token",
        "",
        max_age=0,
        httponly=True,
        secure=env_var.FLASK_ENV == "production",
        samesite="Lax",
    )
    return response
