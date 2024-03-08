import os
from dotenv import load_dotenv

load_dotenv()

FLASK_APP = os.getenv('FLASK_APP')
FLASK_ENV = os.getenv('FLASK_ENV')
YOUR_CHANNEL_ACCESS_TOKEN = os.getenv('YOUR_CHANNEL_ACCESS_TOKEN')
YOUR_CHANNEL_SECRET = os.getenv('YOUR_CHANNEL_SECRET')
DATABASE_URL = os.getenv('EXTERNAL_DATABASE_URL')
DATABASE_NAME = os.getenv('DATABASE_NAME')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
SERVER_ADMIN_LINE_USER_ID = os.getenv('SERVER_ADMIN_LINE_USER_ID')
JWT_AUTH_PATH = os.getenv('JWT_AUTH_PATH', 'auth')
FONT_FILE_PATH = os.getenv('FONT_FILE_PATH', '/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

tmp_server_url = os.getenv('SERVER_URL')
if tmp_server_url is None:
    raise RuntimeError('env var "SERVER_URL" is not set.')
SERVER_URL = tmp_server_url + ("/" if tmp_server_url[-1] != "/" else "")
