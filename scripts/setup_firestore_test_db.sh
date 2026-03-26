#!/usr/bin/env bash
set -euo pipefail

# Firestore テスト用 DB セットアップスクリプト
#
# GCP プロジェクト mahjang-manager 内に Enterprise + MongoDB 互換モードの
# テスト用 Firestore DB を作成し、MongoDB ユーザーと IAM 権限を設定する。
#
# 前提条件:
#   - gcloud CLI がインストール・認証済み
#   - Firestore API が有効化済み
#
# 使い方:
#   bash scripts/setup_firestore_test_db.sh

PROJECT_ID="mahjang-manager"
PROJECT_NUMBER="794762347679"
TEST_DB_NAME="mahjong-manager-test"
REGION="asia-northeast1"
MONGO_USER="test-ci-user"
SA_NAME="firestore-test-ci"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "=== Firestore Test DB Setup ==="
echo "Project: ${PROJECT_ID}"
echo "Test DB: ${TEST_DB_NAME}"
echo "Region:  ${REGION}"
echo ""

# 1. テスト用 Firestore データベース作成 (Enterprise + MongoDB 互換)
echo "[1/5] Creating Firestore database '${TEST_DB_NAME}' (Enterprise + MongoDB compat)..."
if gcloud firestore databases describe --database="${TEST_DB_NAME}" --project="${PROJECT_ID}" &>/dev/null; then
    echo "  Database '${TEST_DB_NAME}' already exists. Skipping."
    echo "  NOTE: If it was created as STANDARD, delete and re-run this script."
    echo "        MongoDB compat requires Enterprise edition."
else
    ACCESS_TOKEN=$(gcloud auth print-access-token)
    curl -s -X POST \
      "https://firestore.googleapis.com/v1/projects/${PROJECT_ID}/databases?databaseId=${TEST_DB_NAME}" \
      -H "Authorization: Bearer ${ACCESS_TOKEN}" \
      -H "Content-Type: application/json" \
      -d "{
        \"type\": \"FIRESTORE_NATIVE\",
        \"locationId\": \"${REGION}\",
        \"databaseEdition\": \"ENTERPRISE\",
        \"mongodbCompatibleDataAccessMode\": \"DATA_ACCESS_MODE_ENABLED\",
        \"firestoreDataAccessMode\": \"DATA_ACCESS_MODE_DISABLED\"
      }" | python3 -m json.tool
    echo "  Created."
fi
echo ""

# 2. MongoDB ユーザー作成 (SCRAM-SHA-256)
echo "[2/5] Creating MongoDB user '${MONGO_USER}'..."
CREDS_OUTPUT=$(gcloud firestore user-creds create "${MONGO_USER}" \
    --database="${TEST_DB_NAME}" \
    --project="${PROJECT_ID}" 2>&1) || {
    if echo "${CREDS_OUTPUT}" | grep -q "ALREADY_EXISTS"; then
        echo "  User '${MONGO_USER}' already exists. Skipping."
    else
        echo "  ERROR: ${CREDS_OUTPUT}"
        exit 1
    fi
}
echo "${CREDS_OUTPUT}"
echo ""
echo "  IMPORTANT: Save the securePassword above! It is shown only once."
echo ""

# 3. MongoDB ユーザーに IAM 権限付与
echo "[3/5] Granting datastore.user to MongoDB user..."
PRINCIPAL="principal://firestore.googleapis.com/projects/${PROJECT_NUMBER}/name/databases/${TEST_DB_NAME}/userCreds/${MONGO_USER}"
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="${PRINCIPAL}" \
    --role="roles/datastore.user" \
    --condition=None \
    --quiet > /dev/null 2>&1
echo "  Granted roles/datastore.user to ${MONGO_USER}."
echo ""

# 4. CI 用サービスアカウント作成 + キー生成
echo "[4/5] Setting up CI service account '${SA_NAME}'..."
if gcloud iam service-accounts describe "${SA_EMAIL}" --project="${PROJECT_ID}" &>/dev/null; then
    echo "  Service account already exists."
else
    gcloud iam service-accounts create "${SA_NAME}" \
        --display-name="Firestore Test CI" \
        --project="${PROJECT_ID}"
    echo "  Created."
fi

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/datastore.user" \
    --condition=None \
    --quiet > /dev/null 2>&1
echo "  Granted roles/datastore.user to SA."

KEY_FILE="firestore-test-sa-key.json"
if [ -f "${KEY_FILE}" ]; then
    echo "  Key file '${KEY_FILE}' already exists. Skipping."
else
    gcloud iam service-accounts keys create "${KEY_FILE}" \
        --iam-account="${SA_EMAIL}" \
        --project="${PROJECT_ID}"
    echo "  Key saved to ${KEY_FILE}"
fi
echo ""

# 5. DB UID 取得 (接続 URL 用)
echo "[5/5] Retrieving database UID..."
DB_UID=$(gcloud firestore databases describe \
    --database="${TEST_DB_NAME}" \
    --project="${PROJECT_ID}" \
    --format="value(uid)" 2>/dev/null)
echo "  DB UID: ${DB_UID}"
echo ""

echo "=== Setup Complete ==="
echo ""
echo "Connection URL format:"
echo "  mongodb://${MONGO_USER}:<PASSWORD>@${DB_UID}.${REGION}.firestore.goog:443/${TEST_DB_NAME}?loadBalanced=true&authMechanism=SCRAM-SHA-256&tls=true&retryWrites=false"
echo ""
echo "GitHub Secrets to register:"
echo "  - FIRESTORE_TEST_DATABASE_URL: (connection URL above with actual password)"
echo "  - GCP_SA_KEY_FIRESTORE_TEST: contents of ${KEY_FILE}"
echo ""
echo "GitHub Variable to register:"
echo "  - FIRESTORE_COMPAT_ENABLED: true"
echo ""
echo "Local test:"
echo "  FIRESTORE_TEST_DATABASE_URL='<url>' pytest tests/firestore_compat/ -v"
echo ""
echo "IMPORTANT: Do NOT commit ${KEY_FILE} to git!"
