# ============================================================
# Stage 1: React フロントエンドをビルド
# ============================================================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# 依存関係を先にコピーしてインストール（キャッシュ活用）
COPY frontend/package*.json ./
RUN npm ci

# ソースをコピーしてビルド
COPY frontend/ ./
RUN npm run build

# ============================================================
# Stage 2: Python / Flask アプリ
# ============================================================
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# システムパッケージ（日本語フォント）
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# Python 依存関係
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリのソースをコピー
COPY . .

# Stage 1 で生成した React ビルド成果物をコピー
# （COPY . . で古い dist が入っていても上書きして最新に保つ）
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

ENV FLASK_APP=src/server

EXPOSE 8080

CMD ["sh", "-c", "gunicorn src.server:app --bind 0.0.0.0:${PORT:-8080} --workers=1 --threads=8 --timeout=60 --log-file=-"]
