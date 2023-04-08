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
# from db_setting import Engine, Session
from ApplicationModels.PageContents import PageContents, RegisterFormData
from use_cases.CreateDummyUseCase import CreateDummyUseCase

from use_cases.web.ViewRegisterUseCase import ViewRegisterUseCase
from use_cases.web.RegisterWebUserUseCase import RegisterWebUserUseCase


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


@views_blueprint.route('/register', methods=['GET'])
def view_register():
    page_contents = PageContents[RegisterFormData](
        session, request, RegisterFormData)
    page_contents, forms = ViewRegisterUseCase().execute(
        page_contents=page_contents
    )
    return render_template(
        'register.html',
        page_contents=page_contents,
        form=forms
    )


@views_blueprint.route('/register', methods=['POST'])
def register():
    page_contents = PageContents(session, request)
    RegisterWebUserUseCase().execute(page_contents=page_contents)
    return render_template(
        'index.html',
        page_contents=page_contents,
    )


@views_blueprint.route('/create_dummy', methods=['POST'])
def create_dummy():
    CreateDummyUseCase().execute()
    return 'Done'

# @views_blueprint.route('/migrate', methods=['POST'])
# def migrate():
    # from db_models import Base, MatchModel
    # MatchModel.add_column(engine=Engine, column_name="tip_scores")

    # return redirect(url_for('views_blueprint.index', message='migrateしました'))


# @views_blueprint.route('/migrate_reset_sequence', methods=['POST'])
# def migrate_reset_sequence():
#     table_name = request.form['table_name']  # ex. users
#     Engine.execute(
#         f'SELECT setval(\'{table_name}_id_seq\', MAX(id)) FROM {table_name};')


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
