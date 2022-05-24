from typing import Dict, List
from xml.dom import NotFoundErr
from flask import (
    Blueprint,
    abort,
    request,
    render_template,
    url_for,
    redirect,
    send_from_directory,
)

from db_setting import Engine, Session
from db_models import Base
from repositories import user_match_repository
from use_cases.CreateDummyUseCase import CreateDummyUseCase

from use_cases.web.GetUsersForWebUseCase import GetUsersForWebUseCase
from use_cases.web.GetYakumanUsersForWebUseCase import GetYakumanUsersForWebUseCase
from use_cases.web.GetConfigsForWebUseCase import GetConfigsForWebUseCase
from use_cases.web.GetHanchansForWebUseCase import GetHanchansForWebUseCase
from use_cases.web.GetGroupsForWebUseCase import GetGroupsForWebUseCase
from use_cases.web.GetMatchesForWebUseCase import GetMatchesForWebUseCase
from use_cases.web.GetUserMatchesForWebUseCase import GetUserMatchesForWebUseCase

from use_cases.web.GetUserForWebUseCase import GetUserForWebUseCase
from use_cases.web.GetYakumanUserForWebUseCase import GetYakumanUserForWebUseCase
from use_cases.web.GetGroupForWebUseCase import GetGroupForWebUseCase
from use_cases.web.GetHanchanForWebUseCase import GetHanchanForWebUseCase
from use_cases.web.GetMatchForWebUseCase import GetMatchForWebUseCase
from use_cases.web.GetUserMatchForWebUseCase import GetUserMatchForWebUseCase
from use_cases.web.GetConfigForWebUseCase import GetConfigForWebUseCase

from use_cases.web.DeleteConfigsForWebUseCase import DeleteConfigsForWebUseCase
from use_cases.web.DeleteMatchesForWebUseCase import DeleteMatchesForWebUseCase
from use_cases.web.DeleteGroupsForWebUseCase import DeleteGroupsForWebUseCase
from use_cases.web.DeleteHanchansForWebUseCase import DeleteHanchansForWebUseCase
from use_cases.web.DeleteUsersForWebUseCase import DeleteUsersForWebUseCase
from use_cases.web.DeleteYakumanUsersForWebUseCase import DeleteYakumanUsersForWebUseCase

from use_cases.web.UpdateUserForWebUseCase import UpdateUserForWebUseCase
from use_cases.web.UpdateYakumanUserForWebUseCase import UpdateYakumanUserForWebUseCase
from use_cases.web.UpdateGroupForWebUseCase import UpdateGroupForWebUseCase
from use_cases.web.UpdateHanchanForWebUseCase import UpdateHanchanForWebUseCase
from use_cases.web.UpdateMatchForWebUseCase import UpdateMatchForWebUseCase
from use_cases.web.UpdateConfigForWebUseCase import UpdateConfigForWebUseCase

from use_cases.web.CreateUserForWebUseCase import CreateUserForWebUseCase
from use_cases.web.CreateYakumanUserForWebUseCase import CreateYakumanUserForWebUseCase
from use_cases.web.CreateGroupForWebUseCase import CreateGroupForWebUseCase
from use_cases.web.CreateHanchanForWebUseCase import CreateHanchanForWebUseCase
from use_cases.web.CreateMatchForWebUseCase import CreateMatchForWebUseCase
from use_cases.web.CreateConfigForWebUseCase import CreateConfigForWebUseCase


from linebot import WebhookHandler, exceptions
import env_var

handler = WebhookHandler(env_var.YOUR_CHANNEL_SECRET)
views_blueprint = Blueprint('views_blueprint', __name__, url_prefix='/')


@views_blueprint.route('/')
def index():
    if request.args.get('message') is not None:
        message = request.args.get('message')
    else:
        message = ''
    return render_template('index.html', title='home', message=message)


@views_blueprint.route('/reset', methods=['POST'])
def reset_db():
    Base.metadata.drop_all(bind=Engine)
    Base.metadata.create_all(bind=Engine)
    return redirect(url_for('views_blueprint.index', message='DBをリセットしました。'))


@views_blueprint.route('/create_dummy', methods=['POST'])
def create_dummy():
    CreateDummyUseCase().execute()
    return 'Done'


@views_blueprint.route('/migrate', methods=['POST'])
def migrate():
    from repositories import match_repository, session_scope
    with session_scope() as session:
        matches = match_repository.find_all(session)
        for m in matches:
            m.hanchan_ids = list(map(int, m.hanchan_ids))
            match_repository.update(session, m)

    return redirect(url_for('views_blueprint.index', message='migrateしました'))


@views_blueprint.route('/migrate_reset_sequence', methods=['POST'])
def migrate_reset_sequence():
    table_name = request.form['table_name']  # ex. users
    Engine.execute(
        f'SELECT setval(\'{table_name}_id_seq\', MAX(id)) FROM {table_name};')


@views_blueprint.route('/migrate_rename_columns', methods=['POST'])
def migrate_rename_columns():
    table_name = request.form['table_name']
    before_name = request.form['before_name']
    after_name = request.form['after_name']
    Engine.execute(
        f'ALTER TABLE {table_name} RENAME COLUMN {before_name} TO {after_name};')

    return redirect(url_for('views_blueprint.index', message='migrateしました'))


@views_blueprint.route('/migrate_create_user_match', methods=['POST'])
def migrate_create_user_match():
    session = Session()
    from db_models import UserMatchModel
    from repositories import hanchan_repository
    from line_models.Profile import Profile
    from DomainService import user_service
    hanchans: List = hanchan_repository.find_all(session)
    target_user_match = []
    for hanchan in hanchans:
        if not isinstance(hanchan.converted_scores, Dict):
            continue
        for user_id in hanchan.converted_scores:
            pro = Profile(display_name='', user_id=user_id)
            res = user_service.find_or_create_by_profile(pro)
            target_user_match.append((res._id, hanchan.match_id))
    for t in set(target_user_match):
        user_match = UserMatchModel(
            user_id=t[0],
            match_id=t[1],
        )
        user_match_repository.create(session, user_match)

    return redirect(url_for('views_blueprint.index', message='migrateしました'))


@views_blueprint.route('/users')
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


@views_blueprint.route('/users/<_id>')
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


@views_blueprint.route('/users/create', methods=['POST'])
def create_user():
    CreateUserForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_users'))


@views_blueprint.route('/users/update', methods=['POST'])
def update_user():
    UpdateUserForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_users'))


@views_blueprint.route('/users/delete', methods=['POST'])
def delete_users():
    target_id = request.args.get('target_id')
    DeleteUsersForWebUseCase().execute([int(target_id)])
    return redirect(url_for('views_blueprint.get_users'))


@views_blueprint.route('/groups')
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


@views_blueprint.route('/groups/<_id>')
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


@views_blueprint.route('/groups/create', methods=['POST'])
def create_group():
    CreateGroupForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_groups'))


@views_blueprint.route('/groups/update', methods=['POST'])
def update_group():
    UpdateGroupForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_groups'))


@views_blueprint.route('/groups/delete', methods=['POST'])
def delete_groups():
    target_id = request.args.get('target_id')
    DeleteGroupsForWebUseCase().execute([int(target_id)])
    return redirect(url_for('views_blueprint.get_groups'))


@views_blueprint.route('/hanchans')
def get_hanchans():
    data = GetHanchansForWebUseCase().execute()
    keys = ['_id', 'line_group_id', 'raw_scores',
            'converted_scores', 'match_id', 'status']
    input_keys = ['line_group_id', 'raw_scores',
                  'converted_scores', 'match_id', 'status']
    return render_template(
        'model.html',
        title='hanchans',
        submit_to='create_hanchan',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@views_blueprint.route('/hanchans/<_id>')
def hanchans_detail(_id):
    data = GetHanchanForWebUseCase().execute(_id)
    if data is None:
        raise NotFoundErr()
    input_keys = ['_id', 'line_group_id', 'raw_scores',
                  'converted_scores', 'match_id', 'status']
    return render_template(
        'detail.html',
        title='hanchans',
        submit_to='update_hanchan',
        input_keys=input_keys,
        init_data=data
    )


@views_blueprint.route('/hanchans/create', methods=['POST'])
def create_hanchan():
    CreateHanchanForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_hanchans'))


@views_blueprint.route('/hanchans/update', methods=['POST'])
def update_hanchan():
    UpdateHanchanForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_hanchans'))


@views_blueprint.route('/hanchans/delete', methods=['POST'])
def delete_hanchans():
    target_id = request.args.get('target_id')
    DeleteHanchansForWebUseCase().execute([int(target_id)])
    return redirect(url_for('views_blueprint.get_hanchans'))


@views_blueprint.route('/matches')
def get_matches():
    data = GetMatchesForWebUseCase().execute()
    keys = [
        '_id',
        'line_group_id',
        'hanchan_ids',
        'created_at',
        'status',
        'users']
    input_keys = ['line_group_id', 'hanchan_ids', 'status']
    return render_template(
        'model.html',
        title='matches',
        submit_to='create_match',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@views_blueprint.route('/matches/<_id>')
def matches_detail(_id):
    data = GetMatchForWebUseCase().execute(_id)
    if data is None:
        raise NotFoundErr()
    input_keys = ['_id', 'line_group_id', 'hanchan_ids', 'status']
    return render_template(
        'detail.html',
        title='matches',
        submit_to='update_match',
        input_keys=input_keys,
        init_data=data
    )


@views_blueprint.route('/matches/create', methods=['POST'])
def create_match():
    CreateMatchForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_matches'))


@views_blueprint.route('/matches/update', methods=['POST'])
def update_match():
    UpdateMatchForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_matches'))


@views_blueprint.route('/matches/delete', methods=['POST'])
def delete_matches():
    target_id = request.args.get('target_id')
    DeleteMatchesForWebUseCase().execute([int(target_id)])
    return redirect(url_for('views_blueprint.get_matches'))


@views_blueprint.route('/configs')
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


@views_blueprint.route('/configs/<_id>')
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


@views_blueprint.route('/configs/create', methods=['POST'])
def create_config():
    CreateConfigForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_configs'))


@views_blueprint.route('/configs/update', methods=['POST'])
def update_config():
    UpdateConfigForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_configs'))


@views_blueprint.route('/configs/delete', methods=['POST'])
def delete_configs():
    target_id = request.args.get('target_id')
    DeleteConfigsForWebUseCase().execute([int(target_id)])
    return redirect(url_for('views_blueprint.get_configs'))


@views_blueprint.route('/user_matches')
def get_user_matches():
    data = GetUserMatchesForWebUseCase().execute()
    keys = ['_id', 'user_id', 'match_id']
    input_keys = ['user_id', 'match_id']
    return render_template(
        'model.html',
        title='user_matches',
        submit_to='create_user_match',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@views_blueprint.route('/user_matches/<_id>')
def user_matches_detail(_id):
    data = GetUserMatchForWebUseCase().execute(_id)
    if data is None:
        raise NotFoundErr()
    input_keys = ['_id', 'user_id', 'match_id']
    return render_template(
        'detail.html',
        title='user_matches',
        submit_to='update_user_match',
        input_keys=input_keys,
        init_data=data
    )


@views_blueprint.route('/user_matches/create', methods=['POST'])
def create_user_match():
    return redirect(url_for('views_blueprint.get_user_matches'))


@views_blueprint.route('/user_matches/update', methods=['POST'])
def update_user_match():
    return redirect(url_for('views_blueprint.get_user_matches'))


@views_blueprint.route('/user_matches/delete', methods=['POST'])
def delete_user_matches():
    return redirect(url_for('views_blueprint.user_matches'))


@views_blueprint.route('/yakuman_users')
def get_yakuman_users():
    data = GetYakumanUsersForWebUseCase().execute()
    keys = ['_id', 'user_id', 'hanchan_id']
    input_keys = ['user_id', 'hanchan_id']
    return render_template(
        'model.html',
        title='yakuman_users',
        submit_to='create_yakuman_user',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@views_blueprint.route('/yakuman_users/<_id>')
def yakuman_users_detail(_id):
    data = GetYakumanUserForWebUseCase().execute(_id)
    if data is None:
        raise NotFoundErr()
    input_keys = ['_id', 'user_id', 'hanchan_id']
    return render_template(
        'detail.html',
        title='yakuman_users',
        submit_to='update_yakuman_user',
        input_keys=input_keys,
        init_data=data
    )


@views_blueprint.route('/yakuman_users/create', methods=['POST'])
def create_yakuman_user():
    CreateYakumanUserForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_yakuman_users'))


@views_blueprint.route('/yakuman_users/update', methods=['POST'])
def update_yakuman_user():
    UpdateYakumanUserForWebUseCase().execute()
    return redirect(url_for('views_blueprint.get_yakuman_users'))


@views_blueprint.route('/yakuman_users/delete', methods=['POST'])
def delete_yakuman_users():
    target_id = request.args.get('target_id')
    DeleteYakumanUsersForWebUseCase().execute([int(target_id)])
    return redirect(url_for('views_blueprint.get_yakuman_users'))


@views_blueprint.route("/callback", methods=['POST'])
def callback():
    """ Endpoint for LINE messaging API """

    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except exceptions.InvalidSignatureError:
        abort(400)
    return 'OK'


@views_blueprint.route('/uploads/<path:filename>')
def download_file(filename: str):
    return send_from_directory("uploads/",
                               filename, as_attachment=True)
