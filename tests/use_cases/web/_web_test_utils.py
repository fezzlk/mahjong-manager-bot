from contextlib import contextmanager

from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "test-secret"
    return app


@contextmanager
def request_context(app: Flask, form_data=None, session_data=None):
    form_data = form_data or {}
    session_data = session_data or {}
    with app.test_request_context("/", method="POST", data=form_data):
        from flask import session

        for key, value in session_data.items():
            session[key] = value
        yield
