#!/bin/bash
# Secret Manager への初回登録スクリプト（値は対話入力）
# 必要な権限: roles/secretmanager.admin
#
# 使い方:
#   1. PROJECT_ID と SERVICE_ACCOUNT を実際の値に変更
#   2. chmod +x setup_secrets.sh && ./setup_secrets.sh

set -euo pipefail

PROJECT_ID="mahjang-manager"

# Cloud Run が使用するサービスアカウント（デフォルトはコンピュートサービスアカウント）
# 独自のサービスアカウントを使う場合は以下を変更してください
# 例: SERVICE_ACCOUNT="mahjong-bot-sa@${PROJECT_ID}.iam.gserviceaccount.com"
SERVICE_ACCOUNT="$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')-compute@developer.gserviceaccount.com"

secrets=(
  DATABASE_URL
  YOUR_CHANNEL_ACCESS_TOKEN
  YOUR_CHANNEL_SECRET
  GOOGLE_CLIENT_ID
  GOOGLE_CLIENT_SECRET
  GOOGLE_GEMINI_API_KEY
  SERVER_ADMIN_LINE_USER_ID
)

# Secret Manager API を有効化
echo "Enabling Secret Manager API..."
gcloud services enable secretmanager.googleapis.com --project="$PROJECT_ID"

echo ""
echo "=== Secret Manager への登録 ==="
echo "各シークレットの値を入力してください（スキップする場合は空のまま Enter）"
echo ""

for secret in "${secrets[@]}"; do
  read -rsp "Enter value for $secret (empty to skip): " value
  echo
  if [ -z "$value" ]; then
    echo "  -> Skipped $secret"
    continue
  fi

  if gcloud secrets describe "$secret" --project="$PROJECT_ID" &>/dev/null; then
    # 既存のシークレットに新バージョンを追加
    echo -n "$value" | gcloud secrets versions add "$secret" \
      --data-file=- \
      --project="$PROJECT_ID"
    echo "  -> Updated $secret (new version added)"
  else
    # 新規作成
    echo -n "$value" | gcloud secrets create "$secret" \
      --data-file=- \
      --project="$PROJECT_ID"
    echo "  -> Created $secret"
  fi
done

echo ""
echo "=== サービスアカウントへの権限付与 ==="
echo "Service Account: $SERVICE_ACCOUNT"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"
echo "  -> Granted roles/secretmanager.secretAccessor"

echo ""
echo "=== 完了 ==="
echo "登録済みシークレット一覧:"
gcloud secrets list --project="$PROJECT_ID"
echo ""
echo "次のステップ: deploy.sh または cloudbuild.yaml を実行してデプロイしてください"
