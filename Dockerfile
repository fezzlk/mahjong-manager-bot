FROM python:3.11-slim

WORKDIR /app

# Pythonの出力バッファを無効化（ログがリアルタイムに出るように）
ENV PYTHONUNBUFFERED=1

# システムパッケージの更新とフォントのインストール
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# 依存関係を先にコピーしてインストール（キャッシュ最適化）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリのソースをコピー
COPY . .

ENV FLASK_APP=src/server

# Cloud Run expects the container to listen on $PORT (default 8080).
EXPOSE 8080

# threading.local() でスレッドセーフなリクエスト状態管理を実装済みのため
# --workers=1 --threads=8 でマルチスレッド処理を有効化
# (Cloud Run では 1 インスタンス = 1 プロセスが推奨)
CMD ["sh","-c","gunicorn src.server:app --bind 0.0.0.0:${PORT:-8080} --workers=1 --threads=8 --timeout=60 --log-file=-"]
