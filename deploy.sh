#!/bin/bash

# Cloud Runデプロイスクリプト

# プロジェクトIDを設定（実際のプロジェクトIDに変更してください）
PROJECT_ID="mahjang-manager"

# サービス名
SERVICE_NAME="mahjong-manager-bot"

# リージョン
REGION="asia-northeast1"

# イメージ名
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Cloud Run が使用するサービスアカウント
# デフォルトコンピュートSAを使う場合はコメントアウトのまま
# 独自SAを使う場合は以下を有効化してください
# SERVICE_ACCOUNT="mahjong-bot-sa@${PROJECT_ID}.iam.gserviceaccount.com"

echo "Cloud Runデプロイを開始します..."

# プロジェクトを設定
echo "プロジェクトID: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Dockerイメージをビルド
echo "Dockerイメージをビルドしています..."
docker build -t $IMAGE_NAME .

# Container Registryにプッシュ
echo "Container Registryにプッシュしています..."
docker push $IMAGE_NAME

# Cloud Runにデプロイ
echo "Cloud Runにデプロイしています..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars "FLASK_APP=src/server,FLASK_ENV=production,DATABASE_NAME=mahjong-manager,SERVER_URL=https://mahjong-manager-bot-794762347679.asia-northeast1.run.app,JWT_AUTH_PATH=auth,FONT_FILE_PATH=/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc,PORT=8080" \
  --set-secrets "DATABASE_URL=DATABASE_URL:latest,YOUR_CHANNEL_ACCESS_TOKEN=YOUR_CHANNEL_ACCESS_TOKEN:latest,YOUR_CHANNEL_SECRET=YOUR_CHANNEL_SECRET:latest,SERVER_ADMIN_LINE_USER_ID=SERVER_ADMIN_LINE_USER_ID:latest,FLASK_SECRET_KEY=FLASK_SECRET_KEY:latest,JWT_SECRET_KEY=JWT_SECRET_KEY:latest"
  # --service-account "${SERVICE_ACCOUNT}"  # 独自SAを使う場合はコメントを外す

echo "デプロイが完了しました！"
echo "サービスURL: https://mahjong-manager-bot-794762347679.asia-northeast1.run.app"
