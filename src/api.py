from flask import Blueprint

api_blueprint = Blueprint('api_blueprint', __name__, url_prefix='/_api')


@api_blueprint.route('/results')
def api_get_results():
    print('api is not complete')
