"""
Application root
If '$ flask run' is executed, this file is call at first.
"""
import os

import set_local_env  # for local dev env

from db_setting import Engine
from models import Base

from flask import Flask, request, abort, g, render_template, url_for, redirect
from linebot import LineBotApi, WebhookHandler, exceptions
from linebot.models import (
    FollowEvent,
    UnfollowEvent,
    JoinEvent,
    MessageEvent,
    TextMessage,
    ImageMessage,
    PostbackEvent,
)

from router import Router
from services import Services

"""define LINE bot handler"""
handler = WebhookHandler(os.environ["YOUR_CHANNEL_SECRET"])

app = Flask(__name__)

services = Services(app)
router = Router(services)


@app.route('/')
def index():
    if request.args.get('message') is not None:
        message = request.args.get('message')
    else:
        message = ''
    return render_template('index.html', title='home', message=message)


@app.route('/reset', methods=['POST'])
def reset_db():
    Base.metadata.drop_all(bind=Engine)
    Base.metadata.create_all(bind=Engine)
    services.app_service.logger.info('reset DB')
    return redirect(url_for('index', message='DBをリセットしました。'))


@app.route('/users')
def get_users():
    data = services.user_service.get_all()
    keys = ['id', 'name', 'user_id', 'mode', 'rooms', 'matches']
    return render_template(
        'table.html',
        title='users',
        keys=keys,
        data=data
    )


@app.route('/users/delete', methods=['POST'])
def delete_users():
    target_id = request.args.get('target_id')
    services.user_service.delete(int(target_id))
    return redirect(url_for('get_users'))


@app.route('/rooms')
def get_rooms():
    data = services.room_service.get_all()
    keys = ['id', 'room_id', 'mode', 'users']
    return render_template(
        'table.html',
        title='rooms',
        keys=keys,
        data=data
    )


@app.route('/rooms/delete', methods=['POST'])
def delete_rooms():
    target_id = request.args.get('target_id')
    services.room_service.delete(int(target_id))
    return redirect(url_for('get_rooms'))


@app.route('/results')
def get_results():
    data = services.results_service.get_all()
    keys = ['id', 'room_id', 'points', 'result', 'match_id', 'status']
    return render_template(
        'table.html',
        title='results',
        keys=keys,
        data=data
    )


@app.route('/results/delete', methods=['POST'])
def delete_results():
    target_id = request.args.get('target_id')
    services.results_service.delete(int(target_id))
    return redirect(url_for('get_results'))


@app.route('/matches')
def get_matches():
    data = services.matches_service.get_all()
    keys = ['id', 'room_id', 'result_ids', 'created_at', 'status', 'users']
    return render_template(
        'table.html',
        title='matches',
        keys=keys,
        data=data
    )


@app.route('/matches/delete', methods=['POST'])
def delete_matches():
    target_id = request.args.get('target_id')
    services.matches_service.delete(int(target_id))
    return redirect(url_for('get_matches'))


@app.route('/configs')
def get_configs():
    data = services.config_service.get_all()
    keys = ['id', 'key', 'value', 'target_id']
    return render_template(
        'table.html',
        title='configs',
        keys=keys,
        data=data
    )


@app.route('/configs/delete', methods=['POST'])
def delete_configs():
    target_id = request.args.get('target_id')
    services.config_service.delete(int(target_id))
    return redirect(url_for('get_configs'))


"""
receive action from LINE
"""


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except exceptions.InvalidSignatureError:
        abort(400)
    return 'OK'


"""
handle events
"""


@handler.add(FollowEvent)
def handle_follow(event):
    router.root(event)


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    router.root(event)


@handler.add(JoinEvent)
def handle_join(event):
    router.root(event)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    router.root(event)


@ handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    router.root(event)


@ handler.add(PostbackEvent)
def handle_postback(event):
    router.root(event)


if __name__ == "__main__":
    app.run(debug=True)
