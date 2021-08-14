"""
Application root
If '$ flask run' is executed, this file is call at first.
"""
# flake8: noqa

import os
import sys
sys.path.append("/src")

from flask import Flask, logging
app = Flask(__name__)
logger = logging.create_logger(app)

from linebot import WebhookHandler
handler = WebhookHandler(os.environ["YOUR_CHANNEL_SECRET"])

from db_setting import Base, Engine
Base.metadata.create_all(bind=Engine)

from services import Services
services = Services(app)

from router import Router
router = Router(services)

import views
import api
import handle_event

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
