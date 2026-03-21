# flake8: noqa
import sys
import os
import pytest
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# ================================
# 🧩 パス設定
# ================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# ================================
# 🌱 .env 読み込み
# ================================
ENV_PATH = os.path.join(BASE_DIR, ".env")
if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH)
else:
    print(f"⚠️ .env not found at {ENV_PATH}")

# ================================
# 📦 アプリモジュールインポート
# ================================
import env_var
import server
from application_service import reply_service, request_info_service


# ================================
# 🩺 DBヘルスチェック（セッション開始時に1回だけ）
# ================================
def pytest_sessionstart(session):
    """Pytest開始時にDB接続を確認し、失敗したら終了する"""
    try:
        # ping は最小コストの接続確認
        client = MongoClient(env_var.DATABASE_URL)
        client.admin.command("ping")
    except PyMongoError as exc:
        message = "MongoDB is not reachable. Please start the test DB server."
        pytest.exit(message, returncode=1)


# ================================
# 🔄 DBリセット用fixture
# ================================
@pytest.fixture(scope="function", autouse=True)
def reset_services():
    """各テストの前後でDBをクリーンにする"""
    from domain_service.user_service import _cached_get_profile_name
    from mongo_client import mongo_client

    mongo_client.drop_database(env_var.DATABASE_NAME)
    request_info_service.delete_req_info()
    reply_service.reset()
    _cached_get_profile_name.cache_clear()
    yield
