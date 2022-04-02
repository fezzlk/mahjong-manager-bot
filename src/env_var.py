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

tmp_db_url = os.getenv('DATABASE_URL')
DATABASE_URL = tmp_db_url + ("/" if tmp_db_url[-1] != "/" else "")

tmp_server_url = os.getenv('SERVER_URL')
SERVER_URL = tmp_server_url + ("/" if tmp_server_url[-1] != "/" else "")
