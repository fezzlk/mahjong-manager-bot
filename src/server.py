import logging
import logging.config
import os
import sys

# debugpyはpytest実行時にはimportしない
debugpy = None
if not any("pytest" in arg for arg in sys.argv):
    try:
        import debugpy
    except ImportError:
        debugpy = None
from flask import Flask
from flask_bcrypt import Bcrypt

# ===== パス設定 =====
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ===== Flask アプリ初期化 =====
import env_var

app = Flask(__name__)
app.secret_key = env_var.FLASK_SECRET_KEY

# ===== ロギング設定 =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

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
        debugpy.listen(("127.0.0.1", 5678))
        logger.info("Debugger can attach at port 5678...")
    except OSError:
        logger.warning("Debugger port already in use")

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
    app.run(threaded=True, use_reloader=True)
