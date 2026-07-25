from flask import Blueprint

api_blueprint = Blueprint("api_blueprint", __name__, url_prefix="/api/v1")

from . import edits, groups, matches, rankings, users  # noqa: F401
