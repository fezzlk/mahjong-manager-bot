"""
Application root
If '$ flask run' is executed, this file is call at first.
"""
# flake8: noqa

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, logging
app = Flask(__name__)
logger = logging.create_logger(app)

from linebot import WebhookHandler
handler = WebhookHandler(os.environ["YOUR_CHANNEL_SECRET"])

from db_setting import Engine
from models import Base
Base.metadata.create_all(bind=Engine)

from views import views_blueprint
from api import api_blueprint

app.register_blueprint(views_blueprint)
app.register_blueprint(api_blueprint)

from linebot import exceptions
from flask import request, abort

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

import handle_event

if __name__ == '__main__':
    app.run()
