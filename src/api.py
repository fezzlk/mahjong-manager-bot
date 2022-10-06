from middlewares import admin_required
from typing import List
from flask import Blueprint
from DomainModel.entities.User import User
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
# from flask_jwt import jwt_required, current_identity
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


@api_blueprint.route('/users/all')
# @ jwt_required()
@admin_required
def api_get_all_users():
    req_user: User = current_identity
    print(f'Receive a request from user_id = {req_user._id}')

    with session_scope() as session:
        records = user_repository.find_all(session)
        return convert_to_json(records)


@api_blueprint.route('/groups/all')
# @ jwt_required()
@admin_required
def api_get_all_groups():
    req_user: User = current_identity
    print(f'Receive a request from user_id = {req_user._id}')

    with session_scope() as session:
        records = group_repository.find_all(session)
        return convert_to_json(records)


@api_blueprint.route('/hanchans/all')
# @ jwt_required()
@admin_required
def api_get_all_hanchans():
    req_user: User = current_identity
    print(f'Receive a request from user_id = {req_user._id}')

    with session_scope() as session:
        records = hanchan_repository.find_all(session)
        return convert_to_json(records)


@api_blueprint.route('/matches/all')
# @ jwt_required()
@admin_required
def api_get_all_matches():
    req_user: User = current_identity
    print(f'Receive a request from user_id = {req_user._id}')

    with session_scope() as session:
        records = match_repository.find_all(session)
        return convert_to_json(records)


@api_blueprint.route('/configs/all')
# @ jwt_required()
@admin_required
def api_get_all_configs():
    req_user: User = current_identity
    print(f'Receive a request from user_id = {req_user._id}')

    with session_scope() as session:
        records = config_repository.find_all(session)
        return convert_to_json(records)
