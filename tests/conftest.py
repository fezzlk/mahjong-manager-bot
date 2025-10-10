# flake8: noqa
import sys
import os
import pytest
from dotenv import load_dotenv

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
from mongo_client import mongo_client  # src/mongo_client.py
import env_var
import server
from ApplicationService import reply_service, request_info_service


# ================================
# 🔄 DBリセット用fixture
# ================================
@pytest.fixture(scope="function", autouse=True)
def reset_services():
    """各テストの前後でDBをクリーンにする"""
    mongo_client.drop_database(env_var.DATABASE_NAME)
    request_info_service.delete_req_info()
    reply_service.reset()
    yield
    # 必要に応じてtear down処理を追加
