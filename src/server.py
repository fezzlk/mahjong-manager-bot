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
app.secret_key = 'random secret'
logger = logging.create_logger(app)


from jwt_setting import register_jwt
jwt = register_jwt(app)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from oauth_client import oauth
oauth.init_app(app)

from db_setting import Engine
from db_models import Base
Base.metadata.create_all(bind=Engine)

from apis.root import views_blueprint
app.register_blueprint(views_blueprint)
from apis.auth import auth_blueprint
app.register_blueprint(auth_blueprint)
from apis.line import line_blueprint
app.register_blueprint(line_blueprint)
from apis.hanchan import hanchan_blueprint
app.register_blueprint(hanchan_blueprint)
from apis.match import match_blueprint
app.register_blueprint(match_blueprint)
from apis.config import config_blueprint
app.register_blueprint(config_blueprint)
from apis.group import group_blueprint
app.register_blueprint(group_blueprint)
from apis.user import user_blueprint
app.register_blueprint(user_blueprint)


import handle_event

if __name__ == '__main__':
    app.run(threaded=True)
