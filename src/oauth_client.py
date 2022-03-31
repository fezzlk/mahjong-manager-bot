from . import env_var
from authlib.integrations.flask_client import OAuth


oauth = OAuth()
oauth.register(
    name='google',
    client_id=env_var.GOOGLE_CLIENT_ID,
    client_secret=env_var.GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'openid profile email'},
)
