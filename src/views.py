import os
from typing import Dict, List
from flask import Blueprint, abort, request, render_template, url_for, redirect
from db_setting import Engine, Session
from db_models import Base
from use_cases.CreateDummyUseCase import CreateDummyUseCase

from use_cases.web.GetConfigsForWebUseCase import GetConfigsForWebUseCase
from use_cases.web.DeleteConfigsForWebUseCase import DeleteConfigsForWebUseCase
from use_cases.web.GetMatchesForWebUseCase import GetMatchesForWebUseCase
from use_cases.web.DeleteMatchesForWebUseCase import DeleteMatchesForWebUseCase
from use_cases.web.GetGroupsForWebUseCase import GetGroupsForWebUseCase
from use_cases.web.DeleteGroupsForWebUseCase import DeleteGroupsForWebUseCase
from use_cases.web.GetHanchansForWebUseCase import GetHanchansForWebUseCase
from use_cases.web.DeleteHanchansForWebUseCase import DeleteHanchansForWebUseCase
from use_cases.web.DeleteUsersForWebUseCase import DeleteUsersForWebUseCase
from use_cases.web.GetUsersForWebUseCase import GetUsersForWebUseCase

from linebot import WebhookHandler, exceptions

handler = WebhookHandler(os.environ["YOUR_CHANNEL_SECRET"])
views_blueprint = Blueprint('views_blueprint', __name__, url_prefix='/')


@views_blueprint.route('/')
def index():
    if request.args.get('message') is not None:
        message = request.args.get('message')
    else:
        message = ''
    return render_template('index.html', title='home', message=message)


# @app.route('/plot')
# def plot():
#     matches_use_cases.plot()
#     return render_template('index.html', title='home', message='message')


@views_blueprint.route('/reset', methods=['POST'])
def reset_db():
    Base.metadata.drop_all(bind=Engine)
    Base.metadata.create_all(bind=Engine)
    return redirect(url_for('views_blueprint.index', message='DBをリセットしました。'))


@views_blueprint.route('/create_dummy', methods=['POST'])
def create_dummy():
    CreateDummyUseCase().execute()
    return 'Done'

# @views_blueprint.route('/try', methods=['POST'])
# def hogehoge():
#     # from repositories import user_repository
#     # from entities.User import User, UserMode
#     session = Session()
#     # user = User(
#     #     line_user_name="test user6",
#     #     line_user_id="U0123456789abcdefghijklmnopqrstu6",
#     #     zoom_url="https://us00web.zoom.us/j/01234567896?pwd=abcdefghijklmnopqrstuvwxyz",
#     #     mode=UserMode.wait,
#     #     jantama_name="jantama user6",
#     #     matches=[1],
#     # )
#     # user_repository.create(session, user)
#     from models import UserMatchModel
#     user_match = UserMatchModel(
#         user_id=2,
#         match_id=1,
#     )
#     session.add(user_match)
#     session.commit()


@views_blueprint.route('/migrate', methods=['POST'])
def migrate():
    session = Session()
    from db_models import UserMatchModel
    from Repositories.HanchanRepository import HanchanRepository
    from services.UserService import UserService
    from models.Profile import Profile
    repository = HanchanRepository()
    service = UserService()
    hanchans: List = repository.find_all(session)
    target_user_match = []
    for hanchan in hanchans:
        if not isinstance(hanchan.converted_scores, Dict):
            continue
        for user_id in hanchan.converted_scores:
            pro = Profile(display_name='', user_id=user_id)
            res = service.find_or_create_by_profile(pro)
            target_user_match.append((res._id, hanchan.match_id))
    for t in set(target_user_match):
        user_match = UserMatchModel(
            user_id=t[0],
            match_id=t[1],
        )
        session.add(user_match)
    # Engine.execute('SELECT setval(\'users_id_seq\', MAX(id)) FROM users;')
    # Engine.execute('SELECT setval(\'groups_id_seq\', MAX(id)) FROM groups;')
    # Engine.execute(
    #     'SELECT setval(\'hanchans_id_seq\', MAX(id)) FROM hanchans;')
    # Engine.execute('SELECT setval(\'matches_id_seq\', MAX(id)) FROM matches;')
    # Engine.execute('SELECT setval(\'configs_id_seq\', MAX(id)) FROM configs;')
    # table_name = request.form['table_name']
    # before_name = request.form['before_name']
    # after_name = request.form['after_name']
    # Engine.execute(f'ALTER TABLE {table_name} RENAME COLUMN {before_name} TO {after_name};')
    session.commit()

    return redirect(url_for('views_blueprint.index', message='migrateしました'))


@views_blueprint.route('/users')
def get_users():
    data = GetUsersForWebUseCase().execute()
    keys = ['_id', 'line_user_name', 'line_user_id', 'jantama_name',
            'zoom_url', 'mode', 'matches', 'groups']
    input_keys = ['line_user_name', 'line_user_id', 'zoom_url', 'jantama_name']
    return render_template(
        'model.html',
        title='users',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@views_blueprint.route('/users/create', methods=['POST'])
def create_users():
    # line_user_name = request.form['line_user_name']
    # user_id = request.form['user_id']
    # user_use_cases.create(line_user_name, user_id)
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
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@views_blueprint.route('/groups/create', methods=['POST'])
def create_groups():
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
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@views_blueprint.route('/hanchans/create', methods=['POST'])
def create_hanchans():
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
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@views_blueprint.route('/matches/create', methods=['POST'])
def create_matches():
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
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@views_blueprint.route('/configs/create', methods=['POST'])
def create_configs():
    return redirect(url_for('views_blueprint.get_configs'))


@views_blueprint.route('/configs/delete', methods=['POST'])
def delete_configs():
    target_id = request.args.get('target_id')
    DeleteConfigsForWebUseCase().execute([int(target_id)])
    return redirect(url_for('views_blueprint.get_configs'))


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
