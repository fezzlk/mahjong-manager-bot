"""
views
"""

from flask import request, abort, render_template, url_for, redirect
from server import Base, Engine
from models import Users, Rooms, Results, Hanchans

from server import app

@app.route('/')
def index():
    if request.args.get('message') is not None:
        message = request.args.get('message')
    else:
        message = ''
    return render_template('index.html', title='home', message=message)


@app.route('/plot')
def plot():
    services.matches_service.plot()
    return render_template('index.html', title='home', message='message')


@app.route('/reset', methods=['POST'])
def reset_db():
    Base.metadata.drop_all(bind=Engine)
    Base.metadata.create_all(bind=Engine)
    services.app_service.logger.info('reset DB')
    return redirect(url_for('index', message='DBをリセットしました。'))


@app.route('/migrate', methods=['POST'])
def migrate():
    # Rooms.add_column(Engine, 'zoom_url')
    # Users.add_column(Engine, 'zoom_id')
    # Users.add_column(Engine, 'jantama_name')
    # services.results_service.migrate()
    res = services.app_service.db.session\
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
        services.app_service.db.session.add(h)
    services.app_service.db.session.commit()

    services.app_service.logger.info('migrate')
    return redirect(url_for('index', message='migrateしました'))


@app.route('/users')
def get_users():
    data = services.user_service.get()
    keys = ['id', 'name', 'user_id', 'jantama_name',
            'zoom_id', 'mode', 'rooms', 'matches']
    input_keys = ['name', 'user_id', 'jantama_name']
    return render_template(
        'model.html',
        title='users',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@app.route('/users/create', methods=['POST'])
def create_users():
    name = request.form['name']
    user_id = request.form['user_id']
    services.user_service.create(name, user_id)
    return redirect(url_for('get_users'))


@app.route('/users/delete', methods=['POST'])
def delete_users():
    target_id = request.args.get('target_id')
    services.user_service.delete(int(target_id))
    return redirect(url_for('get_users'))


@app.route('/rooms')
def get_rooms():
    data = services.room_service.get()
    keys = ['id', 'room_id', 'zoom_url', 'mode', 'users']
    input_keys = ['room_id', 'zoom_url']
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
    services.room_service.delete(int(target_id))
    return redirect(url_for('get_rooms'))


@app.route('/hanchans')
def get_hanchans():
    data = services.hanchans_service.get()
    keys = ['id', 'room_id', 'raw_scores',
            'converted_scores', 'match_id', 'status']
    input_keys = ['room_id', 'raw_scores',
                  'convertes_scores', 'match_id', 'status']
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
    # target_id = request.args.get('target_id')
    # services.hanchans_service.delete(int(target_id))
    return redirect(url_for('get_hanchans'))


@app.route('/results')
def get_results():
    data = services.results_service.get()
    keys = ['id', 'room_id', 'points', 'result', 'match_id', 'status']
    input_keys = ['room_id', 'points', 'result', 'match_id', 'status']
    return render_template(
        'model.html',
        title='results',
        keys=keys,
        input_keys=input_keys,
        data=data
    )


@app.route('/results/create', methods=['POST'])
def create_results():
    return redirect(url_for('get_results'))


@app.route('/results/delete', methods=['POST'])
def delete_results():
    target_id = request.args.get('target_id')
    services.results_service.delete(int(target_id))
    return redirect(url_for('get_results'))


@app.route('/matches')
def get_matches():
    data = services.matches_service.get()
    keys = ['id', 'room_id', 'result_ids', 'created_at', 'status', 'users']
    input_keys = ['room_id', 'result_ids', 'status']
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
    services.matches_service.delete(int(target_id))
    return redirect(url_for('get_matches'))


@app.route('/configs')
def get_configs():
    data = services.config_service.get()
    keys = ['id', 'key', 'value', 'target_id']
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
    services.config_service.delete(int(target_id))
    return redirect(url_for('get_configs'))
    

""" Endpoint for LINE messaging API """
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except exceptions.InvalidSignatureError:
        abort(400)
    return 'OK'
