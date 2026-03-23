from authlib.integrations.flask_client import OAuth

import env_var

oauth = OAuth()
oauth.register(
    name="line",
    client_id=env_var.LINE_LOGIN_CHANNEL_ID,
    client_secret=env_var.LINE_LOGIN_CHANNEL_SECRET,
    authorize_url="https://access.line.me/oauth2/v2.1/authorize",
    access_token_url="https://api.line.me/oauth2/v2.1/token",
    client_kwargs={"scope": "profile openid"},
)
