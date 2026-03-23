#!/bin/bash
set -euo pipefail

# Cloud Runデプロイスクリプト

# プロジェクトIDを設定（実際のプロジェクトIDに変更してください）
PROJECT_ID="mahjang-manager"

# サービス名
SERVICE_NAME="mahjong-manager-bot"

# リージョン
REGION="asia-northeast1"

# イメージ名（ロールバック用にタグ付き + latest の2本立て）
GIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"
IMAGE_TAG="${IMAGE_NAME}:${GIT_SHA}"
IMAGE_LATEST="${IMAGE_NAME}:latest"

# Cloud Run が使用するサービスアカウント
# デフォルトコンピュートSAを使う場合はコメントアウトのまま
# 独自SAを使う場合は以下を有効化してください
# SERVICE_ACCOUNT="mahjong-bot-sa@${PROJECT_ID}.iam.gserviceaccount.com"

echo "Cloud Runデプロイを開始します..."
echo "プロジェクトID: $PROJECT_ID"
echo "イメージタグ: $IMAGE_TAG"

# Dockerイメージをビルド（SHA タグと latest タグの両方）
echo "Dockerイメージをビルドしています..."
docker build -t "$IMAGE_TAG" -t "$IMAGE_LATEST" .

# Container Registryにプッシュ
echo "Container Registryにプッシュしています..."
docker push "$IMAGE_TAG"
docker push "$IMAGE_LATEST"

# Cloud Runにデプロイ（ロールバック可能な SHA タグを使用）
echo "Cloud Runにデプロイしています..."
gcloud run deploy $SERVICE_NAME \
  --project "$PROJECT_ID" \
  --image "$IMAGE_TAG" \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300 \
  --health-check-http-path=/health \
  --set-env-vars "FLASK_APP=src/server,FLASK_ENV=production,DATABASE_NAME=mahjong-manager,SERVER_URL=https://mahjong-manager-bot-794762347679.asia-northeast1.run.app,JWT_AUTH_PATH=auth,FONT_FILE_PATH=/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc,PORT=8080,GCS_BUCKET_NAME=mahjong-manager-images" \
  --set-secrets "DATABASE_URL=DATABASE_URL:latest,YOUR_CHANNEL_ACCESS_TOKEN=YOUR_CHANNEL_ACCESS_TOKEN:latest,YOUR_CHANNEL_SECRET=YOUR_CHANNEL_SECRET:latest,SERVER_ADMIN_LINE_USER_ID=SERVER_ADMIN_LINE_USER_ID:latest,FLASK_SECRET_KEY=FLASK_SECRET_KEY:latest,JWT_SECRET_KEY=JWT_SECRET_KEY:latest,LINE_LOGIN_CHANNEL_ID=LINE_LOGIN_CHANNEL_ID:latest,LINE_LOGIN_CHANNEL_SECRET=LINE_LOGIN_CHANNEL_SECRET:latest"
  # --service-account "${SERVICE_ACCOUNT}"  # 独自SAを使う場合はコメントを外す

echo "デプロイが完了しました！"
echo "サービスURL: https://mahjong-manager-bot-794762347679.asia-northeast1.run.app"
echo "イメージタグ: $IMAGE_TAG"
echo "ロールバック例: gcloud run deploy $SERVICE_NAME --image ${IMAGE_NAME}:<前のタグ> --project $PROJECT_ID --region $REGION"
