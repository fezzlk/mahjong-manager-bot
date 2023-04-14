from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    url_for,
)
from xml.dom import NotFoundErr
from use_cases.web.GetConfigForWebUseCase import GetConfigForWebUseCase
from use_cases.web.GetConfigsForWebUseCase import GetConfigsForWebUseCase
from use_cases.web.UpdateConfigForWebUseCase import UpdateConfigForWebUseCase
from use_cases.web.DeleteConfigsForWebUseCase import DeleteConfigsForWebUseCase

config_blueprint = Blueprint(
    'config_blueprint',
    __name__,
    url_prefix='/config'
)


@config_blueprint.route('/')
def get_configs():
    data = GetConfigsForWebUseCase().execute()
    keys = ['_id', 'key', 'value', 'target_id']
    input_keys = ['key', 'value', 'target_id']
    return render_template(
        'model.html',
        title='configs',
        submit_to='create_config',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@config_blueprint.route('/<_id>')
def configs_detail(_id):
    data = GetConfigForWebUseCase().execute(_id)
    if data is None:
        raise NotFoundErr()
    input_keys = ['_id', 'key', 'value', 'target_id']
    return render_template(
        'detail.html',
        title='configs',
        submit_to='update_config',
        input_keys=input_keys,
        init_data=data
    )


@config_blueprint.route('/create', methods=['POST'])
def create_config():
    return redirect(url_for('config_blueprint.get_configs'))


@config_blueprint.route('/update', methods=['POST'])
def update_config():
    UpdateConfigForWebUseCase().execute()
    return redirect(url_for('config_blueprint.get_configs'))


@config_blueprint.route('/delete', methods=['POST'])
def delete_configs():
    target_id = request.args.get('target_id')
    DeleteConfigsForWebUseCase().execute([int(target_id)])
    return redirect(url_for('config_blueprint.get_configs'))
