from flask import Blueprint

api_blueprint = Blueprint("api_blueprint", __name__, url_prefix="/api/v1")

from . import groups, matches, rankings, users  # noqa: E402, F401
