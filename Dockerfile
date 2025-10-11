FROM python:3.10-slim

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