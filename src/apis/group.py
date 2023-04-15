from flask import (
    Blueprint,
    redirect,
    request,
    render_template,
    url_for,
)
from xml.dom import NotFoundErr
from use_cases.web.GetGroupsForWebUseCase import GetGroupsForWebUseCase
from use_cases.web.GetGroupForWebUseCase import GetGroupForWebUseCase
from use_cases.web.UpdateGroupForWebUseCase import UpdateGroupForWebUseCase
from use_cases.web.DeleteGroupsForWebUseCase import DeleteGroupsForWebUseCase

group_blueprint = Blueprint(
    'group_blueprint',
    __name__,
    url_prefix='/group'
)


@group_blueprint.route('/')
def get_groups():
    data = GetGroupsForWebUseCase().execute()
    keys = ['_id', 'line_group_id', 'zoom_url', 'mode', 'users']
    input_keys = ['line_group_id', 'zoom_url']
    return render_template(
        'model.html',
        title='groups',
        submit_to='create_group',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@group_blueprint.route('/<_id>')
def groups_detail(_id):
    data = GetGroupForWebUseCase().execute(_id)
    if data is None:
        raise NotFoundErr()
    input_keys = ['_id', 'line_group_id', 'zoom_url']
    return render_template(
        'detail.html',
        title='groups',
        submit_to='update_group',
        input_keys=input_keys,
        init_data=data
    )


@group_blueprint.route('/create', methods=['POST'])
def create_group():
    return redirect(url_for('views_blueprint.get_groups'))


@group_blueprint.route('/update', methods=['POST'])
def update_group():
    UpdateGroupForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_groups'))


@group_blueprint.route('/delete', methods=['POST'])
def delete_groups():
    target_id = request.args.get('target_id')
    DeleteGroupsForWebUseCase().execute([int(target_id)])
    return redirect(url_for('views_blueprint.get_groups'))
