from flask import Blueprint, request, render_template, url_for, redirect
from db_setting import Engine
from models import Base
from models import Results, Hanchans
from db_setting import Session
from use_cases import (
    get_configs_for_web_use_case,
    get_hanchans_for_web_use_case,
    get_matches_for_web_use_case,
    get_rooms_for_web_use_case,
    get_users_for_web_use_case,
    delete_configs_for_web_use_case,
    delete_hanchans_for_web_use_case,
    delete_matches_for_web_use_case,
    delete_rooms_for_web_use_case,
    delete_users_for_web_use_case,
)

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
    return redirect(url_for('index', message='DBをリセットしました。'))


@views_blueprint.route('/migrate', methods=['POST'])
def migrate():
    # Rooms.add_column(Engine, 'zoom_url')
    # Users.add_column(Engine, 'zoom_id')
    # Users.add_column(Engine, 'jantama_name')
    # results_service.migrate()
    session = Session()
    res = session\
        .query(Results).all()
    for r in res:
        h = Hanchans(
            id=r.id,
            room_id=r.room_id,
            raw_scores=r.points,
            converted_scores=r.result,
            match_id=r.match_id,
            status=r.status,
        )
        session.add(h)
    session.commit()

    return redirect(url_for('index', message='migrateしました'))


@views_blueprint.route('/users')
def get_users():
    data = get_users_for_web_use_case.execute()
    keys = ['_id', 'name', 'line_user_id', 'jantama_name',
            'zoom_url', 'mode', 'matches', 'rooms']
    input_keys = ['name', 'line_user_id', 'zoom_url', 'jantama_name']
    return render_template(
        'model.html',
        title='users',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@views_blueprint.route('/users/create', methods=['POST'])
def create_users():
    # name = request.form['name']
    # user_id = request.form['user_id']
    # user_use_cases.create(name, user_id)
    return redirect(url_for('get_users'))


@views_blueprint.route('/users/delete', methods=['POST'])
def delete_users():
    target_id = request.args.get('target_id')
    delete_users_for_web_use_case.execute([int(target_id)])
    return redirect(url_for('get_users'))


@views_blueprint.route('/rooms')
def get_rooms():
    data = get_rooms_for_web_use_case.execute()
    keys = ['_id', 'line_room_id', 'zoom_url', 'mode', 'users']
    input_keys = ['line_room_id', 'zoom_url']
    return render_template(
        'model.html',
        title='rooms',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@views_blueprint.route('/rooms/create', methods=['POST'])
def create_rooms():
    return redirect(url_for('get_rooms'))


@views_blueprint.route('/rooms/delete', methods=['POST'])
def delete_rooms():
    target_id = request.args.get('target_id')
    delete_rooms_for_web_use_case.execute([int(target_id)])
    return redirect(url_for('get_rooms'))


@views_blueprint.route('/hanchans')
def get_hanchans():
    data = get_hanchans_for_web_use_case.execute()
    keys = ['_id', 'line_room_id', 'raw_scores',
            'converted_scores', 'match_id', 'status']
    input_keys = ['line_room_id', 'raw_scores',
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
    return redirect(url_for('get_hanchans'))


@views_blueprint.route('/hanchans/delete', methods=['POST'])
def delete_hanchans():
    target_id = request.args.get('target_id')
    delete_hanchans_for_web_use_case.execute([int(target_id)])
    return redirect(url_for('get_hanchans'))


@views_blueprint.route('/matches')
def get_matches():
    data = get_matches_for_web_use_case.execute()
    keys = ['_id', 'line_room_id', 'hanchan_ids', 'created_at', 'status', 'users']
    input_keys = ['line_room_id', 'hanchan_ids', 'status']
    return render_template(
        'model.html',
        title='matches',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@views_blueprint.route('/matches/create', methods=['POST'])
def create_matches():
    return redirect(url_for('get_matches'))


@views_blueprint.route('/matches/delete', methods=['POST'])
def delete_matches():
    target_id = request.args.get('target_id')
    delete_matches_for_web_use_case.execute([int(target_id)])
    return redirect(url_for('get_matches'))


@views_blueprint.route('/configs')
def get_configs():
    data = get_configs_for_web_use_case.execute()
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
    return redirect(url_for('get_configs'))


@views_blueprint.route('/configs/delete', methods=['POST'])
def delete_configs():
    target_id = request.args.get('target_id')
    delete_configs_for_web_use_case.execute([int(target_id)])
    return redirect(url_for('get_configs'))
