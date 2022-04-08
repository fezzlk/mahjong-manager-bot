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


from jwt_setting import register_jwt
from datetime import datetime
jwt = register_jwt(app)

@jwt.jwt_payload_handler
def make_payload(identity):
    iat = datetime.utcnow()
    exp = iat + app.config.get('JWT_EXPIRATION_DELTA') 
    nbf = iat + app.config.get('JWT_NOT_BEFORE_DELTA')
    identity = getattr(identity, '_id')
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}


from db_setting import Engine
from db_models import Base
Base.metadata.create_all(bind=Engine)

from views import views_blueprint
from api import api_blueprint

app.register_blueprint(views_blueprint)
app.register_blueprint(api_blueprint)

import handle_event

if __name__ == '__main__':
    app.run(threaded=True)
