# from typing import Dict, List
# from xml.dom import NotFoundErr
from flask import (
    Blueprint,
    abort,
    request,
    render_template,
    url_for,
    redirect,
    session,
    send_from_directory,
)
from db_setting import Engine
from ApplicationModels.PageContents import PageContents
from use_cases.CreateDummyUseCase import CreateDummyUseCase
from middlewares import login_required

from linebot import WebhookHandler, exceptions
import env_var

handler = WebhookHandler(env_var.YOUR_CHANNEL_SECRET)
views_blueprint = Blueprint('views_blueprint', __name__, url_prefix='/')


@views_blueprint.route('/')
def index():
    page_contents = PageContents(session, request)
    if request.args.get('message') is not None:
        page_contents.message = request.args.get('message')
    return render_template('index.html', page_contents=page_contents)


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
    return send_from_directory(
        "uploads/",
        filename,
        as_attachment=True
    )


@views_blueprint.route('/login', methods=['GET'])
def view_login():
    page_contents = PageContents(session, request)
    return render_template(
        'login.html',
        page_contents=page_contents,
    )


@views_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views_blueprint.view_login'))


@views_blueprint.route('/create_dummy', methods=['POST'])
@login_required
def create_dummy():
    CreateDummyUseCase().execute()
    return 'Done'


@views_blueprint.route('/migrate', methods=['GET'])
def migrate():
    from DomainModel.entities.UserGroup import UserGroup
    from repositories import (
        session_scope, 
        hanchan_repository,
        user_group_repository, 
        group_repository, 
        user_repository,
    )
    with session_scope() as db_session:
        hanchans = hanchan_repository.find_all(session=db_session)
        list = []
        for h in hanchans:
            if type(h.converted_scores) is not dict:
                continue

            group = group_repository.find_one_by_line_group_id(
                session=db_session, line_group_id=h.line_group_id
            )
            if group is None:
                continue

            for u_id, _ in h.converted_scores.items():
                user = user_repository.find_one_by_line_user_id(
                    session=db_session, line_user_id=u_id
                )
                if user is None:
                    continue
  
                list.append((h.line_group_id, u_id))
        for s in set(list):
            user_group_repository.create(
                session=db_session,
                new_user_group=UserGroup(
                    line_user_id=s[1],
                    line_group_id=s[0],
                )
            )

    return 'migrateしました'

# @views_blueprint.route('/migrate', methods=['POST'])
# def migrate():
    # from db_models import Base, MatchModel
    # MatchModel.add_column(engine=Engine, column_name="tip_scores")

    # return redirect(url_for('views_blueprint.index', message='migrateしました'))


@views_blueprint.route('/migrate_reset_sequence', methods=['POST'])
def migrate_reset_sequence():
    Engine.execute('SELECT setval(\'users_id_seq\', MAX(id)) FROM users;')
    Engine.execute('SELECT setval(\'matches_id_seq\', MAX(id)) FROM matches;')
    Engine.execute('SELECT setval(\'hanchans_id_seq\', MAX(id)) FROM hanchans;')
    Engine.execute('SELECT setval(\'configs_id_seq\', MAX(id)) FROM configs;')
    Engine.execute('SELECT setval(\'groups_id_seq\', MAX(id)) FROM groups;')


# @views_blueprint.route('/migrate_rename_columns', methods=['POST'])
# def migrate_rename_columns():
#     table_name = request.form['table_name']
#     before_name = request.form['before_name']
#     after_name = request.form['after_name']
#     Engine.execute(
#         f'ALTER TABLE {table_name} RENAME COLUMN {before_name} TO {after_name};')

#     return redirect(url_for('views_blueprint.index', message='migrateしました'))


# @views_blueprint.route('/migrate_create_user_match', methods=['POST'])
# def migrate_create_user_match():
#     from repositories import user_match_repository
#     db_session = Session()
#     from db_models import UserMatchModel
#     from repositories import hanchan_repository
#     from line_models.Profile import Profile
#     from DomainService import user_service
#     hanchans: List = hanchan_repository.find_all(db_session)
#     target_user_match = []
#     for hanchan in hanchans:
#         if not isinstance(hanchan.converted_scores, Dict):
#             continue
#         for user_id in hanchan.converted_scores:
#             pro = Profile(display_name='', user_id=user_id)
#             res = user_service.find_or_create_by_profile(pro)
#             target_user_match.append((res._id, hanchan.match_id))
#     for t in set(target_user_match):
#         user_match = UserMatchModel(
#             user_id=t[0],
#             match_id=t[1],
#         )
#         user_match_repository.create(db_session, user_match)

#     return redirect(url_for('views_blueprint.index', message='migrateしました'))
