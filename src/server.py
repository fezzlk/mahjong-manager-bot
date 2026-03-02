import logging
import logging.config
import os
import sys
from pathlib import Path

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

# React ビルド成果物のパス（プロジェクトルートからの相対）
_FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"

app = Flask(
    __name__,
    static_folder=str(_FRONTEND_DIST / "assets"),
    static_url_path="/assets",
)
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

from apis.api import api_blueprint

app.register_blueprint(api_blueprint)

from apis.line import line_blueprint

app.register_blueprint(line_blueprint)

from apis.group import group_blueprint

app.register_blueprint(group_blueprint)

from apis.config import config_blueprint

app.register_blueprint(config_blueprint)

from apis.web_user import web_user_blueprint

app.register_blueprint(web_user_blueprint)


# ===== React SPA フォールバック =====
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_spa(path: str):
    """React の index.html を返す(/api, /auth, /callback, /health, /uploads は除外済み)"""
    from flask import send_from_directory  # noqa: PLC0415

    index = _FRONTEND_DIST / "index.html"
    if index.exists():
        return send_from_directory(str(_FRONTEND_DIST), "index.html")
    return "Frontend not built. Run: cd frontend && npm run build", 404


if __name__ == "__main__":
    app.run(threaded=True, use_reloader=True)
