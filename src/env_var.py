import os
from dotenv import load_dotenv

load_dotenv()

FLASK_APP = os.getenv('FLASK_APP')
FLASK_ENV = os.getenv('FLASK_ENV')
FLASK_DEBUG = os.getenv('FLASK_DEBUG')
IS_TEMPORARY_BUILD = os.getenv('IS_TEMPORARY_BUILD')
YOUR_CHANNEL_ACCESS_TOKEN = os.getenv('YOUR_CHANNEL_ACCESS_TOKEN')
YOUR_CHANNEL_SECRET = os.getenv('YOUR_CHANNEL_SECRET')
DATABASE_URL = os.getenv('DATABASE_URL')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
SERVER_ADMIN_LINE_USER_ID = os.getenv('SERVER_ADMIN_LINE_USER_ID')

tmp_server_url = os.getenv('SERVER_URL')
SERVER_URL = None
if tmp_server_url is None:
    print('Warning: env var "tmp_server_url" is not set.')
else:
    SERVER_URL = tmp_server_url + ("/" if tmp_server_url[-1] != "/" else "")
