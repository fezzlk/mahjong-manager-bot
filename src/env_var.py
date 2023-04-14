import os
from dotenv import load_dotenv

load_dotenv()

FLASK_APP = os.getenv('FLASK_APP')
FLASK_ENV = os.getenv('FLASK_ENV')
FLASK_DEBUG = os.getenv('FLASK_DEBUG')
IS_TEMPORARY_BUILD = os.getenv('IS_TEMPORARY_BUILD')
YOUR_CHANNEL_ACCESS_TOKEN = os.getenv('YOUR_CHANNEL_ACCESS_TOKEN')
YOUR_CHANNEL_SECRET = os.getenv('YOUR_CHANNEL_SECRET')
DATABASE_URL = os.getenv('EXTERNAL_DATABASE_URL') if os.getenv('IS_TEST') is None else os.getenv('EXTERNAL_DATABASE_URL_FOR_TEST')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
SERVER_ADMIN_LINE_USER_ID = os.getenv('SERVER_ADMIN_LINE_USER_ID')
ADMIN_LINE_USER_ID_LIST_JSON = os.getenv('ADMIN_LINE_USER_ID_LIST_JSON')
JWT_AUTH_PATH = os.getenv('JWT_AUTH_PATH', 'auth')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

tmp_server_url = os.getenv('SERVER_URL')
if tmp_server_url is None:
    raise RuntimeError('env var "SERVER_URL" is not set.')
SERVER_URL = tmp_server_url + ("/" if tmp_server_url[-1] != "/" else "")
