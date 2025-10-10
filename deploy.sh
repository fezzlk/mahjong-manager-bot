#!/bin/bash

# Cloud Runデプロイスクリプト

# プロジェクトIDを設定（実際のプロジェクトIDに変更してください）
PROJECT_ID="your-gcp-project-id"

# サービス名
SERVICE_NAME="mahjong-manager-bot"

# リージョン
REGION="asia-northeast1"

# イメージ名
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Cloud Runデプロイを開始します..."

# プロジェクトを設定
echo "📋 プロジェクトID: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Dockerイメージをビルド
echo "🔨 Dockerイメージをビルドしています..."
docker build -t $IMAGE_NAME .

# Container Registryにプッシュ
echo "📤 Container Registryにプッシュしています..."
docker push $IMAGE_NAME

# Cloud Runにデプロイ
echo "🚀 Cloud Runにデプロイしています..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars FLASK_ENV=production,PORT=8080

echo "✅ デプロイが完了しました！"
echo "🌐 サービスURL: https://$SERVICE_NAME-$PROJECT_ID.a.run.app"
