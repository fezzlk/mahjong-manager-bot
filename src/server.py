import os
import sys
import requests

from dotenv import load_dotenv
import env_var

# debugpyはpytest実行時にはimportしない
debugpy = None
if not any("pytest" in arg for arg in sys.argv):
    try:
        import debugpy
    except ImportError:
        debugpy = None
from flask import Flask, logging
from flask_bcrypt import Bcrypt

# ===== パス設定 =====
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# ===== 環境変数ロード =====
load_dotenv()
# ===== Flask アプリ初期化 =====
# ===== Flask アプリ初期化 =====
app = Flask(__name__)
app.secret_key = "random secret"
logger = logging.create_logger(app)


# ===== LINE BotID取得 =====
def get_bot_info():
    url = 'https://api.line.me/v2/bot/info'
    headers = {
        'Authorization': f'Bearer {env_var.YOUR_CHANNEL_ACCESS_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    return response.json()


# ===== debugpy (ホットリロード対応) =====
# WERKZEUG_RUN_MAIN はリロード用サブプロセス判定用
# pytest実行時はdebugpyを使用しない
if (
    debugpy is not None
    and not any("pytest" in arg for arg in sys.argv)
    and os.environ.get("FLASK_DEBUG_ATTACH") == "1"
    and os.environ.get("WERKZEUG_RUN_MAIN") == "true"
):
    try:
        debugpy.listen(("0.0.0.0", 5678))
        print("🔍 Debugger can attach at port 5678...")
    except OSError:
        print("⚠️ Debugger port already in use")

# ===== Flask 拡張 =====
from jwt_setting import register_jwt

jwt = register_jwt(app)
bcrypt = Bcrypt(app)
from oauth_client import oauth

oauth.init_app(app)

# ===== Blueprint登録 =====
from apis.root import views_blueprint

app.register_blueprint(views_blueprint)
from apis.auth import auth_blueprint

app.register_blueprint(auth_blueprint)


if __name__ == "__main__":
    # 起動時にLINE BOTIDを取得する
    info = get_bot_info()
    bot_id = info.get("userId")
    os.environ["YOUR_BOT_LINE_ID"] = bot_id
    
    app.run(threaded=True, use_reloader=True)
    

