from flask import request, abort, render_template, url_for, redirect
from linebot import exceptions
from db_setting import Engine
from models import Base
from server import app, handler, logger
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

print('call views.py')


@app.route('/')
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


@app.route('/reset', methods=['POST'])
def reset_db():
    Base.metadata.drop_all(bind=Engine)
    Base.metadata.create_all(bind=Engine)
    logger.info('reset DB')
    return redirect(url_for('index', message='DBをリセットしました。'))


@app.route('/migrate', methods=['POST'])
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

    logger.info('migrate')
    return redirect(url_for('index', message='migrateしました'))


@app.route('/users')
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


@app.route('/users/create', methods=['POST'])
def create_users():
    # name = request.form['name']
    # user_id = request.form['user_id']
    # user_use_cases.create(name, user_id)
    return redirect(url_for('get_users'))


@app.route('/users/delete', methods=['POST'])
def delete_users():
    target_id = request.args.get('target_id')
    delete_users_for_web_use_case.execute([int(target_id)])
    return redirect(url_for('get_users'))


@app.route('/rooms')
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


@app.route('/rooms/create', methods=['POST'])
def create_rooms():
    return redirect(url_for('get_rooms'))


@app.route('/rooms/delete', methods=['POST'])
def delete_rooms():
    target_id = request.args.get('target_id')
    delete_rooms_for_web_use_case.execute([int(target_id)])
    return redirect(url_for('get_rooms'))


@app.route('/hanchans')
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


@app.route('/hanchans/create', methods=['POST'])
def create_hanchans():
    return redirect(url_for('get_hanchans'))


@app.route('/hanchans/delete', methods=['POST'])
def delete_hanchans():
    target_id = request.args.get('target_id')
    delete_hanchans_for_web_use_case.execute([int(target_id)])
    return redirect(url_for('get_hanchans'))


@app.route('/matches')
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


@app.route('/matches/create', methods=['POST'])
def create_matches():
    return redirect(url_for('get_matches'))


@app.route('/matches/delete', methods=['POST'])
def delete_matches():
    target_id = request.args.get('target_id')
    delete_matches_for_web_use_case.execute([int(target_id)])
    return redirect(url_for('get_matches'))


@app.route('/configs')
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


@app.route('/configs/create', methods=['POST'])
def create_configs():
    return redirect(url_for('get_configs'))


@app.route('/configs/delete', methods=['POST'])
def delete_configs():
    target_id = request.args.get('target_id')
    delete_configs_for_web_use_case.execute([int(target_id)])
    return redirect(url_for('get_configs'))


@app.route("/callback", methods=['POST'])
def callback():
    """ Endpoint for LINE messaging API """

    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except exceptions.InvalidSignatureError:
        abort(400)
    return 'OK'
