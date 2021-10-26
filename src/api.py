from flask import Blueprint

api_blueprint = Blueprint('api_blueprint', __name__, url_prefix='/_api')


@api_blueprint.route('/users')
def api_get_users():
    print('api is not complete')


@api_blueprint.route('/groups')
def api_get_groups():
    print('api is not complete')


@api_blueprint.route('/hanchans')
def api_get_hanchans():
    print('api is not complete')


@api_blueprint.route('/matches')
def api_get_matches():
    print('api is not complete')


@api_blueprint.route('/configs')
def api_get_configs():
    print('api is not complete')
