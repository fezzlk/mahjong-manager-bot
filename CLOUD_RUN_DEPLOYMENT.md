# Cloud Run デプロイメント手順

このドキュメントでは、麻雀マネージャーボットを Google Cloud Run にデプロイする手順を説明します。

## 前提条件

1. Google Cloud Platform アカウント
2. Google Cloud SDK (gcloud) のインストール
3. Docker のインストール
4. プロジェクトの作成と課金の有効化

## 1. 事前準備

### 1.1 Google Cloud プロジェクトの設定

```bash
# プロジェクトIDを設定
export PROJECT_ID="your-gcp-project-id"

# プロジェクトを設定
gcloud config set project $PROJECT_ID

# 必要なAPIを有効化
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### 1.2 認証設定

```bash
# Google Cloudにログイン
gcloud auth login

# Docker認証を設定
gcloud auth configure-docker
```

## 2. Secret Manager のセットアップ

機密情報（DB URL・LINE トークン等）は Google Secret Manager で管理します。
`--set-env-vars` での平文設定は行いません。

### 2.1 シークレットの登録

```bash
# setup_secrets.sh のプロジェクトIDを編集してから実行
chmod +x setup_secrets.sh
./setup_secrets.sh
```

スクリプトは以下を行います:
- Secret Manager API の有効化
- 7件のシークレットを対話形式で登録（既存シークレットは新バージョン追加）
- Cloud Run サービスアカウントへの `roles/secretmanager.secretAccessor` 付与

### 2.2 サービスアカウントについて

Cloud Run はデフォルトでプロジェクトのコンピュートサービスアカウント
（`<PROJECT_NUMBER>-compute@developer.gserviceaccount.com`）を使用します。

独自のサービスアカウントを使う場合は `setup_secrets.sh` と `deploy.sh` / `cloudbuild.yaml` 内の
`SERVICE_ACCOUNT` / `--service-account` の設定を変更してください。

> **注意**: `.env` に記載された `GOOGLE_APPLICATION_CREDENTIALS` は別プロジェクトの古い認証情報です。
> Cloud Run は ADC (Application Default Credentials) で自動認証されるため `GOOGLE_APPLICATION_CREDENTIALS` は不要です。

### 2.3 登録済みシークレットの確認

```bash
gcloud secrets list --project=$PROJECT_ID
```

## 3. データベース設定

### 3.1 Firestore with MongoDB compatibility の設定

1. Firestore で MongoDB compatibility を有効化（Enterprise edition）
2. データベースを作成（Database ID を確認）
3. MongoDB 互換の接続エンドポイント（UID / Location）を確認
4. 必要に応じて SCRAM ユーザーを作成
5. 接続文字列を取得  
   例:
   ```
   mongodb://<UID>.<LOCATION>.firestore.goog:443/<DATABASE_ID>?loadBalanced=true&tls=true&retryWrites=false
   ```
   SCRAM 認証を使う場合:
   ```
   mongodb://<USERNAME>:<PASSWORD>@<UID>.<LOCATION>.firestore.goog:443/<DATABASE_ID>?loadBalanced=true&authMechanism=SCRAM-SHA-256&tls=true&retryWrites=false
   ```

### 3.2 DATABASE_URL の設定

`DATABASE_URL` は Secret Manager に登録してください（`setup_secrets.sh` 参照）。
接続文字列の形式は `env.cloudrun.example` を参照。

## 4. デプロイ方法

### 方法 1: 自動デプロイスクリプトを使用

```bash
# deploy.shのプロジェクトIDを編集
vim deploy.sh

# デプロイを実行
./deploy.sh
```

### 方法 2: 手動デプロイ

```bash
# 1. Dockerイメージをビルド
docker build -t gcr.io/$PROJECT_ID/mahjong-manager-bot .

# 2. Container Registryにプッシュ
docker push gcr.io/$PROJECT_ID/mahjong-manager-bot

# 3. Cloud Runにデプロイ
gcloud run deploy mahjong-manager-bot \
  --image gcr.io/$PROJECT_ID/mahjong-manager-bot \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars "FLASK_APP=src/server,FLASK_ENV=production,DATABASE_NAME=your_db_name,SERVER_URL=https://your-cloudrun-url.run.app,JWT_AUTH_PATH=auth,FONT_FILE_PATH=/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc,PORT=8080" \
  --set-secrets "DATABASE_URL=DATABASE_URL:latest,YOUR_CHANNEL_ACCESS_TOKEN=YOUR_CHANNEL_ACCESS_TOKEN:latest,YOUR_CHANNEL_SECRET=YOUR_CHANNEL_SECRET:latest,GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID:latest,GOOGLE_CLIENT_SECRET=GOOGLE_CLIENT_SECRET:latest,GOOGLE_GEMINI_API_KEY=GOOGLE_GEMINI_API_KEY:latest,SERVER_ADMIN_LINE_USER_ID=SERVER_ADMIN_LINE_USER_ID:latest"
```

### 方法 3: Cloud Build を使用

```bash
# Cloud Buildでデプロイ
gcloud builds submit --config cloudbuild.yaml .
```

## 5. デプロイ後の確認

### 5.1 サービス URL の確認（Secret Manager の確認も）

```bash
# 登録済みシークレットの確認
gcloud secrets list --project=$PROJECT_ID

# Cloud Run の Variables & Secrets タブでもマウント状況を確認できます
```

### 5.2 サービス URL の確認

```bash
gcloud run services describe mahjong-manager-bot \
  --region asia-northeast1 \
  --format 'value(status.url)'
```

### 5.3 ログの確認

```bash
gcloud logs tail --service mahjong-manager-bot
```

### 5.4 ヘルスチェック

```bash
curl https://your-service-url.run.app/
```

## 6. トラブルシューティング

### 6.1 よくある問題

4. **Secret Manager 権限エラー**

   - Cloud Run サービスアカウントに `roles/secretmanager.secretAccessor` が付与されているか確認
   - `setup_secrets.sh` の IAM 付与ステップが成功しているか確認
   - `gcloud secrets list` でシークレットが存在するか確認

1. **データベース接続エラー**

   - Firestore with MongoDB compatibility の接続文字列を確認（`loadBalanced=true&tls=true&retryWrites=false` が必須）
   - SCRAM 認証を使う場合はユーザー/パスワードを確認

2. **LINE Bot の応答エラー**

   - Channel Access Token と Channel Secret が正しいか確認
   - Webhook URL が正しく設定されているか確認

3. **メモリ不足エラー**
   - Cloud Run のメモリ設定を 1Gi 以上に増やす

### 6.2 ログの確認

```bash
# リアルタイムログ
gcloud logs tail --service mahjong-manager-bot

# 特定の時間範囲のログ
gcloud logs read --service mahjong-manager-bot --since 1h
```

## 7. 継続的デプロイの設定

### 7.1 GitHub Actions の設定

`.github/workflows/deploy.yml`を作成：

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Google Cloud SDK
        uses: google-github-actions/setup-gcloud@v0
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}

      - name: Deploy to Cloud Run
        run: |
          gcloud builds submit --config cloudbuild.yaml .
```

## 8. セキュリティ考慮事項

1. **環境変数の管理**

   - 機密情報は Google Secret Manager を使用
   - 環境変数ではなく、シークレットとして管理

2. **ネットワークセキュリティ**

   - 必要に応じて認証を有効化
   - VPC コネクタの使用を検討

3. **データベースセキュリティ**
   - Firestore with MongoDB compatibility の接続設定を確認（ネットワーク設定や認証）
   - データベースユーザーの権限最小化

## 9. コスト最適化

1. **インスタンス設定**

   - 最小インスタンス数を 0 に設定
   - 最大インスタンス数を適切に設定

2. **リソース設定**
   - 必要最小限のメモリと CPU を設定
   - タイムアウト設定の最適化

---

この手順に従って、麻雀マネージャーボットを Cloud Run にデプロイできます。
