from flask import (
    Blueprint,
    request,
    render_template,
    url_for,
    redirect,
)
from xml.dom import NotFoundErr
from use_cases.web.GetUserForWebUseCase import GetUserForWebUseCase
from use_cases.web.GetUsersForWebUseCase import GetUsersForWebUseCase
from use_cases.web.UpdateUserForWebUseCase import UpdateUserForWebUseCase
from use_cases.web.DeleteUsersForWebUseCase import DeleteUsersForWebUseCase

user_blueprint = Blueprint(
    'user_blueprint',
    __name__,
    url_prefix='/user'
)


@user_blueprint.route('/')
def get_users():
    data = GetUsersForWebUseCase().execute()
    keys = ['_id', 'line_user_name', 'line_user_id', 'jantama_name',
            'zoom_url', 'mode', 'matches', 'groups']
    input_keys = [
        'line_user_name',
        'line_user_id',
        'zoom_url',
        'jantama_name']
    return render_template(
        'model.html',
        title='users',
        submit_to='create_user',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@user_blueprint.route('/<_id>')
def users_detail(_id):
    data = GetUserForWebUseCase().execute(_id)
    if data is None:
        raise NotFoundErr()
    input_keys = [
        '_id',
        'line_user_name',
        'line_user_id',
        'mode',
        'zoom_url',
        'jantama_name']
    return render_template(
        'detail.html',
        title='user_detail',
        submit_to='update_user',
        input_keys=input_keys,
        init_data=data
    )


@user_blueprint.route('/create', methods=['POST'])
def create_user():
    # line_user_name = request.form['line_user_name']
    # user_id = request.form['user_id']
    # user_use_cases.create(line_user_name, user_id)
    return redirect(url_for('views_blueprint.get_users'))


@user_blueprint.route('/update', methods=['POST'])
def update_user():
    UpdateUserForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_users'))


@user_blueprint.route('/delete', methods=['POST'])
def delete_users():
    target_id = request.args.get('target_id')
    DeleteUsersForWebUseCase().execute([int(target_id)])
    return redirect(url_for('views_blueprint.get_users'))
