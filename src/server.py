"""
Application root
If '$ flask run' is executed, this file is call at first.
"""

import os
import sys
sys.path.append("/src")

from db_setting import Base, Engine
from flask import Flask
from linebot import WebhookHandler

from router import Router
from services import Services

"""define LINE bot handler"""
handler = WebhookHandler(os.environ["YOUR_CHANNEL_SECRET"])

app = Flask(__name__)

services = Services(app)
router = Router(services)
Base.metadata.create_all(bind=Engine)

import views
import api
import handle_event

if __name__ == '__main__':
    app.run(debug=True, threaded=True)