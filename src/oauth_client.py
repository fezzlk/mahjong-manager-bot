from authlib.integrations.flask_client import OAuth

import env_var

oauth = OAuth()
oauth.register(
    name="google",
    client_id=env_var.GOOGLE_CLIENT_ID,
    client_secret=env_var.GOOGLE_CLIENT_SECRET,
    client_kwargs={"scope": "profile email"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)
