from typing import List
from flask import Blueprint
from repositories import (
    session_scope,
    user_repository,
    group_repository,
    hanchan_repository,
    match_repository,
    config_repository,
)
import json
from datetime import datetime
api_blueprint = Blueprint('api_blueprint', __name__, url_prefix='/_api')


def expire_encoder(object):
    if isinstance(object, datetime):
        return object.isoformat()


def convert_to_json(records: List) -> str:
    return json.dumps(
        [r.__dict__ for r in records],
        default=expire_encoder,
        ensure_ascii=False,
    )


@api_blueprint.route('/users')
def api_get_users():
    with session_scope() as session:
        records = user_repository.find_all(session)
        return convert_to_json(records)


@api_blueprint.route('/groups')
def api_get_groups():
    with session_scope() as session:
        records = group_repository.find_all(session)
        return convert_to_json(records)


@api_blueprint.route('/hanchans')
def api_get_hanchans():
    with session_scope() as session:
        records = hanchan_repository.find_all(session)
        return convert_to_json(records)


@api_blueprint.route('/matches')
def api_get_matches():
    with session_scope() as session:
        records = match_repository.find_all(session)
        return convert_to_json(records)


@api_blueprint.route('/configs')
def api_get_configs():
    with session_scope() as session:
        records = config_repository.find_all(session)
        return convert_to_json(records)
